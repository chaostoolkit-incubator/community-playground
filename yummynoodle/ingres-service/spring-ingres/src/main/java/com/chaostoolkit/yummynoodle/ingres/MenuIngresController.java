package com.chaostoolkit.yummynoodle.ingres;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
public class MenuIngresController {

    //@Autowired
    //private MenuClient client;

    @Bean
    RestTemplate restTemplate() {
        return new RestTemplate();
    }

    @RequestMapping("/menu")
    public String menu() {
        ResponseEntity<String> exchange =
                this.restTemplate().exchange(
                        "http://menu-service/",
                        HttpMethod.GET,
                        null,
                        String.class);

        return exchange.getBody();

    }
}
