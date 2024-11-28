package com.example;

import com.example.service.BedrockService;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.ConfigurableApplicationContext;

import reactor.core.publisher.Mono;
import java.time.Duration;

@SpringBootApplication
public class BedrockClientApplication {
    private static ConfigurableApplicationContext context;

    public static void main(String[] args) {
        context = SpringApplication.run(BedrockClientApplication.class, args);
        context.registerShutdownHook();
    }

    @Bean
    public CommandLineRunner run(BedrockService bedrockService) {
        return args -> {
            String prompt = "write a 1000 words story?";
            System.out.println("Sending prompt to Bedrock: " + prompt);
            
            bedrockService.invokeModel(prompt)
                .doOnNext(chunk -> {
                    System.out.print(chunk);
                    System.out.flush();
                })
                .doOnError(error -> {
                    System.err.println("Error: " + error.getMessage());
                    shutdownGracefully();
                })
                .doOnComplete(() -> {
                    System.out.println("\nStream completed");
                    shutdownGracefully();
                })
                .subscribe();
        };
    }

    private void shutdownGracefully() {
        // Give some time for resources to clean up
        Mono.delay(Duration.ofSeconds(1))
            .subscribe(ignored -> {
                System.exit(0);
            });
    }
}
