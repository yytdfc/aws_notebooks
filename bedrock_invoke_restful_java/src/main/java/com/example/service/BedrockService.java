package com.example.service;

import com.example.aws.AwsRequestSigner;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.nio.charset.StandardCharsets;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.core.io.buffer.DataBuffer;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;

@Service
public class BedrockService {
    private final WebClient webClient;
    private final AwsRequestSigner requestSigner;
    private final String endpoint;
    private final String modelId;
    private final ObjectMapper objectMapper;

    public BedrockService(
            @Value("${aws.access-key}") String accessKey,
            @Value("${aws.secret-key}") String secretKey,
            @Value("${aws.region}") String region,
            @Value("${aws.bedrock.model-id}") String modelId) {
        
        this.endpoint = "https://bedrock-runtime." + region + ".amazonaws.com";
        this.modelId = modelId;
        this.requestSigner = new AwsRequestSigner(accessKey, secretKey, region, "bedrock");
        this.webClient = WebClient.builder().build();
        this.objectMapper = new ObjectMapper();
    }

    public Flux<String> invokeModel(String prompt) {
        String requestBody = createRequestBody(prompt);
        String apiUrl = endpoint + "/model/" + modelId + "/invoke-with-response-stream";
        System.out.println(apiUrl);
        System.out.println(requestBody);

        return webClient.method(HttpMethod.POST)
                .uri(apiUrl)
                .headers(headers -> headers.addAll(requestSigner.generateSignedHeaders(apiUrl, HttpMethod.POST, requestBody)))
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(requestBody)
                .retrieve()
                .bodyToFlux(DataBuffer.class)
                .map(dataBuffer -> {
                    byte[] bytes = new byte[dataBuffer.readableByteCount()];
                    dataBuffer.read(bytes);
                    String chunk = new String(bytes, StandardCharsets.UTF_8);
                    try {
                        // Split the chunk by newlines in case we receive multiple events
                        String[] events = chunk.split("\n");
                        StringBuilder output = new StringBuilder();
                        
                        for (String event : events) {
                            if (event.trim().isEmpty()) continue;
                            
                            // Extract JSON part after "message-typeevent"
                            int jsonStart = event.indexOf("event{");
                            if (jsonStart == -1) continue;
                            
                            // Find the end of JSON by looking for the last '}'
                            int jsonEnd = event.lastIndexOf("}");
                            if (jsonEnd == -1) continue;
                            
                            String jsonStr = event.substring(jsonStart + 5, jsonEnd + 1);
                            JsonNode jsonNode = objectMapper.readTree(jsonStr);
                            
                            if (jsonNode.has("bytes")) {
                                String base64Content = jsonNode.get("bytes").asText();
                                String decodedContent = new String(java.util.Base64.getDecoder().decode(base64Content), StandardCharsets.UTF_8);
                                
                                // Parse the decoded content as JSON to handle different message types
                                JsonNode decodedJson = objectMapper.readTree(decodedContent);
                                
                                if (decodedJson.has("type")) {
                                    String type = decodedJson.get("type").asText();
                                    if (type.equals("content_block_delta")) {
                                        if (decodedJson.has("delta") && decodedJson.has("index")) {
                                            output.append(decodedJson.get("delta").get("text").asText());
                                        }
                                    }
                                    // Handle other message types if needed
                                }
                            }
                        }
                        return output.toString();
                    } catch (Exception e) {
                        System.err.println("Error parsing chunk: " + e.getMessage() + "\nRaw chunk: " + chunk);
                        return "";
                    }
                })
                .filter(content -> !content.isEmpty());
    }

    private String createRequestBody(String prompt) {
        // Format specific to Claude model
        return String.format("""
{
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 2048,
    "messages": [{"role": "user", "content": "%s"}],
    "system": "you are a helpful assistant"
}
""", prompt);
    }
}
