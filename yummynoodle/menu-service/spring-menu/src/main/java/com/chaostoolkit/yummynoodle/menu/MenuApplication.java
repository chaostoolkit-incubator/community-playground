package com.chaostoolkit.yummynoodle.menu;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class MenuApplication {

    @RequestMapping("/")
    public String home() {
        return "I'm alive!!!!";
    }

	public static void main(String[] args) {
		SpringApplication.run(MenuApplication.class, args);
	}

}
