package com.example.aws;

import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.auth.SigningAlgorithm;
import com.amazonaws.util.BinaryUtils;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Map;
import java.util.TreeMap;
import java.net.URLEncoder;

public class AwsRequestSigner {
    private final AWSCredentials credentials;
    private final String region;
    private final String service;

    public AwsRequestSigner(String accessKey, String secretKey, String region, String service) {
        this.credentials = new BasicAWSCredentials(accessKey, secretKey);
        this.region = region;
        this.service = service;
    }

    public HttpHeaders generateSignedHeaders(String endpoint, HttpMethod method, String body) {
        try {
            ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
            String amzDate = now.format(DateTimeFormatter.ofPattern("yyyyMMdd'T'HHmmss'Z'"));
            String dateStamp = now.format(DateTimeFormatter.ofPattern("yyyyMMdd"));

            Map<String, String> headers = new TreeMap<>();
            headers.put("host", new java.net.URL(endpoint).getHost());
            headers.put("x-amz-date", amzDate);
            headers.put("x-amz-content-sha256", calculateContentHash(body));

            String canonicalRequest = createCanonicalRequest(method, endpoint.replace(":0", "%3A0"), "", headers, body);
            String stringToSign = createStringToSign(dateStamp, region, service, canonicalRequest, amzDate);
            String signature = calculateSignature(dateStamp, region, service, stringToSign, credentials.getAWSSecretKey());

            String signedHeaders = String.join(";", headers.keySet());
            String authorizationHeader = String.format(
                "AWS4-HMAC-SHA256 Credential=%s/%s/%s/%s/aws4_request, SignedHeaders=%s, Signature=%s",
                credentials.getAWSAccessKeyId(), dateStamp, region, service, signedHeaders, signature
            );

            HttpHeaders httpHeaders = new HttpHeaders();
            headers.forEach(httpHeaders::set);
            httpHeaders.set("Authorization", authorizationHeader);
            return httpHeaders;
        } catch (Exception e) {
            throw new RuntimeException("Failed to sign AWS request", e);
        }
    }

    private String createCanonicalRequest(HttpMethod method, String endpoint, String canonicalQueryString,
                                        Map<String, String> headers, String payload) throws Exception {
        String canonicalUri = new java.net.URL(endpoint).getPath();
        if (canonicalUri.isEmpty()) {
            canonicalUri = "/";
        }

        String canonicalHeaders = headers.entrySet().stream()
                .map(e -> e.getKey().toLowerCase() + ":" + e.getValue().trim())
                .reduce("", (a, b) -> a + b + "\n");

        String signedHeaders = String.join(";", headers.keySet());

        return String.format("%s\n%s\n%s\n%s\n%s\n%s",
                method.name(),
                canonicalUri,
                canonicalQueryString,
                canonicalHeaders,
                signedHeaders,
                calculateContentHash(payload));
    }

    private String createStringToSign(String dateStamp, String region, String service,
                                    String canonicalRequest, String amzDate) throws Exception {
        String scope = String.format("%s/%s/%s/aws4_request", dateStamp, region, service);
        return String.format("AWS4-HMAC-SHA256\n%s\n%s\n%s",
                amzDate,
                scope,
                hash(canonicalRequest));
    }

    private String calculateSignature(String dateStamp, String region, String service,
                                    String stringToSign, String secretKey) throws Exception {
        byte[] kSecret = ("AWS4" + secretKey).getBytes(StandardCharsets.UTF_8);
        byte[] kDate = sign(dateStamp, kSecret);
        byte[] kRegion = sign(region, kDate);
        byte[] kService = sign(service, kRegion);
        byte[] kSigning = sign("aws4_request", kService);
        return BinaryUtils.toHex(sign(stringToSign, kSigning));
    }

    private String calculateContentHash(String content) throws Exception {
        return hash(content);
    }

    private String hash(String input) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        md.update(input.getBytes(StandardCharsets.UTF_8));
        return BinaryUtils.toHex(md.digest());
    }

    private byte[] sign(String stringData, byte[] key) throws Exception {
        Mac mac = Mac.getInstance(SigningAlgorithm.HmacSHA256.name());
        mac.init(new SecretKeySpec(key, SigningAlgorithm.HmacSHA256.name()));
        return mac.doFinal(stringData.getBytes(StandardCharsets.UTF_8));
    }
}
