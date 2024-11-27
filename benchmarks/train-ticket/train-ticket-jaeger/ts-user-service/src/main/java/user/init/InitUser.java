package user.init;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import user.entity.User;
import user.repository.UserRepository;
import user.service.UserService;


import java.util.UUID;

/**
 * @author fdse
 */
@Component
public class InitUser implements CommandLineRunner {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    protected PasswordEncoder passwordEncoder;

    @Autowired
    private UserService userService;

    @Override
    public void run(String... strings) throws Exception {
//         User whetherExistUser = userRepository.findByUserName("fdse_microservice");
//         User user = User.builder()
//                 .userId("4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f")
//                 .userName("fdse_microservice")
//                 .password("111111")
//                 .gender(1)
//                 .documentType(1)
//                 .documentNum("2135488099312X")
//                 .email("trainticket_notify@163.com").build();
//         user.setUserId("4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f");
//         if (whetherExistUser == null) {
//             userRepository.save(user);
//         }
 List<User> users = Arrays.asList(
        User.builder()
            .userId("4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f")
            .userName("fdse_microservice")
            .password("111111")
            .gender(1)
            .documentType(1)
            .documentNum("2135488099312X")
            .email("trainticket_notify@163.com")
            .build(),
        User.builder()
            .userId("a7d8a66d-81b2-4d6e-8759-bda74a35b77e")
            .userName("fdse_admin")
            .password("admin123")
            .gender(1)
            .documentType(2)
            .documentNum("12345678901234A")
            .email("admin@example.com")
            .build(),
        User.builder()
            .userId("b9fca70f-c23e-4c90-9b7f-780aaf4d5dfe")
            .userName("fdse_user")
            .password("user123")
            .gender(2)
            .documentType(1)
            .documentNum("9876543210987B")
            .email("user@example.com")
            .build()
    );

    for (User user : users) {
            // Vérification si l'utilisateur existe déjà
            User existingUser = userRepository.findByUserName(user.getUserName());

            if (existingUser == null) {
                // Si l'utilisateur n'existe pas, on le sauvegarde
                userRepository.save(user);
                System.out.println("User " + user.getUserName() + " saved!");
            } else {
                System.out.println("User " + user.getUserName() + " already exists.");
            }
        }
    }
}
