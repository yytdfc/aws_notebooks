package org.example;

import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONObject;

import software.amazon.awssdk.services.sagemakerruntime.SageMakerRuntimeClient;
import software.amazon.awssdk.services.sagemakerruntime.model.InvokeEndpointRequest;
import software.amazon.awssdk.services.sagemakerruntime.model.InvokeEndpointResponse;

import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.core.SdkBytes;
import software.amazon.awssdk.regions.Region;


class Document {
    String Title;
    String Content;

    public Document(String title, String content) {
        this.Title = title;
        this.Content = content;
    }

    @Override
    public String toString() {
        return "{\"Title\":\"" + Title + "\",\"Content\":\"" + Content + "\"}";
    }
}


public class Handler {
    private final SageMakerRuntimeClient sagemakerRuntimeClient;

    public Handler() {
		// use the env variable AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY
		// sagemakerRuntimeClient = SageMakerRuntimeClient.builder()
		// 		.credentialsProvider(DefaultCredentialsProvider.create())
		// 		.region(Region.US_EAST_1)
		// 		.build();

        // or

		String accessKey = "xxxxxxxxxxxxxxxxx";
        String secretKey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
		AwsBasicCredentials awsCreds = AwsBasicCredentials.create(accessKey, secretKey);
		sagemakerRuntimeClient = SageMakerRuntimeClient.builder()
				.credentialsProvider(StaticCredentialsProvider.create(awsCreds))
				.region(Region.US_EAST_1)
				.build();
    }

    public static String invokeSpecficEndpoint(SageMakerRuntimeClient runtimeClient, String endpointName, String payload,
            String contentType) {
        InvokeEndpointRequest endpointRequest = InvokeEndpointRequest.builder()
                .endpointName(endpointName)
                .contentType(contentType)
                .body(SdkBytes.fromString(payload, Charset.defaultCharset()))
                .build();

        InvokeEndpointResponse response = runtimeClient.invokeEndpoint(endpointRequest);
        return response.body().asString(Charset.defaultCharset());
    }
        


    public void sendRequest() {
        /*
        Pyaload Args:
            query (str): The search query
            documents (list[str], list[dict]): The documents to rerank
            top_n (int): (optional) The number of results to return, defaults to return all results
            max_chunks_per_doc (int): (optional) The maximum number of chunks derived from a document
            rank_fields (list[str]): (optional) The fields used for reranking. This parameter is only supported for rerank v3 models
        Example:
            {
                "query": "What emails have been about returning items?",
                "documents": [
                    {"Title":"Contraseña incorrecta","Content":"Hola, llevo una hora intentando acceder a mi cuenta y sigue diciendo que mi contraseña es incorrecta. ¿Puede ayudarme, por favor?"},
                    ...
                    {"Title":"Return Defective Product","Content":"Hello, I have a question about the return policy for this product. I purchased it a few weeks ago and it is defective."}
                ],
                "top_n": 2,
                "return_documents": false,
                "max_chunks_per_doc" null,
                "rank_fields": ["Title", "Content"]
            }

        Response format:
            result (list[{"index": document_idx, "relevance_score": float}]): a list of result document and score
        Example:
            {
                "id": "9d366def-6fa5-419b-b92f-a483f2a2e2d8",
                "results": [{
                    "index": 7,
                    "relevance_score": 0.02470387
                }, {
                    "index": 2,
                    "relevance_score": 0.0068771075
                }],
                "meta": {
                    "api_version": {
                        "version": "1"
                    },
                    "billed_units": {
                        "search_units": 1
                    }
                }
            }
         */
        List<Document> documents = new ArrayList<>();
        documents.add(new Document("Contraseña incorrecta", "Hola, llevo una hora intentando acceder a mi cuenta y sigue diciendo que mi contraseña es incorrecta. ¿Puede ayudarme, por favor?"));
        documents.add(new Document("Confirmation Email Missed", "Hi, I recently purchased a product from your website but I never received a confirmation email. Can you please look into this for me?"));
        documents.add(new Document("أسئلة حول سياسة الإرجاع", "مرحبًا، لدي سؤال حول سياسة إرجاع هذا المنتج. لقد اشتريته قبل بضعة أسابيع وهو معيب"));
        documents.add(new Document("Customer Support is Busy", "Good morning, I have been trying to reach your customer support team for the past week but I keep getting a busy signal. Can you please help me?"));
        documents.add(new Document("Falschen Artikel erhalten", "Hallo, ich habe eine Frage zu meiner letzten Bestellung. Ich habe den falschen Artikel erhalten und muss ihn zurückschicken."));
        documents.add(new Document("Customer Service is Unavailable", "Hello, I have been trying to reach your customer support team for the past hour but I keep getting a busy signal. Can you please help me?"));
        documents.add(new Document("Return Policy for Defective Product", "Hi, I have a question about the return policy for this product. I purchased it a few weeks ago and it is defective."));
        documents.add(new Document("收到错误物品", "早上好，关于我最近的订单，我有一个问题。我收到了错误的商品，需要退货。"));
        documents.add(new Document("Return Defective Product", "Hello, I have a question about the return policy for this product. I purchased it a few weeks ago and it is defective."));
        
        StringBuilder documents_string = new StringBuilder();
        for (int i = 0; i < documents.size(); i++) {
            documents_string.append(documents.get(i).toString());
            if (i < documents.size() - 1) {
                documents_string.append(",\n");
            }
        }

        String payload = "{"
            + "\"query\": \"What emails have been about returning items?\","
            + "\"documents\": ["
            + documents_string.toString()
            + "],"
            + "\"top_n\": 2,"
            + "\"return_documents\": false,"
            + "\"max_chunks_per_doc\": null,"
            + "\"rank_fields\": [\"Title\", \"Content\"]"
            + "}";

        String response = invokeSpecficEndpoint(
            sagemakerRuntimeClient,
            "cohere-rerank-multilingual-v3",
            payload,
            "application/json"
        );

        JSONObject jsonObject = new JSONObject(response);

        JSONArray resultsArray = jsonObject.getJSONArray("results");

        System.out.println("Results:");
        for (int i = 0; i < resultsArray.length(); i++) {
            JSONObject result = resultsArray.getJSONObject(i);
            int index = result.getInt("index");
            double relevanceScore = result.getDouble("relevance_score");

            System.out.println("  Index: " + index);
            System.out.println("  Document: " + documents.get(index).toString());
            System.out.println("  Relevance Score: " + relevanceScore);
            System.out.println();
        }

    }
}

