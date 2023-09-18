# 注解

<details>

<summary>@SpringBootApplication</summary>

程序主入口，用于开启自动配置和组件扫描，包含以下三个注解

* @SpringBootConfiguration：标注当前类是一个配置类，相当于传统Spring中的@Configuration注解。
* @EnableAutoConfiguration：开启自动配置，根据项目的依赖和类路径，自动选择合适的配置类加载到容器中。
* @ComponentScan：开启组件扫描，自动发现和注册带有@Component、@Service、@Repository等注解的类。

</details>

<details>

<summary>@RestController</summary>

标注类为控制器，类方法可以作为响应函数

@RestController注解是Spring Boot提供的一种注解，它是在@Controller注解的基础上添加了@ResponseBody注解。@Controller注解用于标识一个类为控制器，而@ResponseBody注解用于指定将方法返回的对象转换为JSON或XML格式的响应体。@RestController注解相当于@Controller + @ResponseBody的组合，可以简化Spring Boot Web开发中的RESTful接口的编写。

</details>

<details>

<summary>@RequestMapping</summary>

它可以用在类或方法上，表示不同层级的请求路径。如果用在类上，表示该类下的所有方法都共享该类的请求路径；如果用在方法上，表示该方法的请求路径是在类的请求路径的基础上追加的。

</details>

<details>

<summary>@GetMapping</summary>

在控制器类或方法上添加，@GetMapping注解是基于@RequestMapping注解实现的，它相当@RequestMapping(method = RequestMethod.GET)的简写形式。

</details>

