# AWS Bedrock Client

A Spring Boot application for interacting with Amazon Bedrock's Claude model using streaming responses.

## Features

- Spring WebFlux for non-blocking HTTP requests
- Streaming responses from Claude model
- AWS Signature V4 authentication
- Reactive programming with Project Reactor

## Prerequisites

- Java 17+
- Maven
- AWS Account with Bedrock access
- AWS credentials

## Configuration

Add to `src/main/resources/application.properties`:

```properties
aws.access-key=your_access_key
aws.secret-key=your_secret_key
aws.region=your_region
aws.bedrock.model-id=us.anthropic.claude-3-5-sonnet-20241022-v2:0
```

## Usage

Build:
```bash
mvn clean install
```

Run:
```bash
mvn spring-boot:run
```

## Project Structure

- `BedrockClientApplication.java`: Main application class with command-line runner for demonstrating model interaction
- `BedrockService.java`: Service layer handling Bedrock API interactions and response streaming
- `AwsRequestSigner.java`: AWS Signature V4 authentication implementation

## Technical Details

### Authentication
The application implements AWS Signature V4 signing process for secure API access to Bedrock services.

### Streaming
Uses WebFlux's reactive streams for non-blocking I/O with real-time content streaming from the Claude model.

## Dependencies

- Spring Boot WebFlux 3.4.0
- AWS Java SDK Core 1.12.261
- Jackson 2.15.3
- Project Lombok 1.18