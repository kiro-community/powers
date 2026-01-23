---
inclusion: fileMatch
fileMatchPattern: "**/websphere-to-springboot.md,**/weblogic-to-springboot.md"
---

# J2EE to Spring Boot Reactive Migration - Common Patterns

This steering file contains common migration patterns shared between WebSphere and WebLogic to Spring Boot Reactive migrations.

## Target Architecture

All J2EE migrations target:
- Spring Boot 3.x with Java 17+
- Fully reactive architecture (WebFlux, R2DBC, Reactor)
- AWS container-based deployments (ECS/EKS)
- Graviton processor optimization
- AWS Java Runtime (Corretto)

## Common Migration Strategy Bank

### Application Server → Spring Boot

| J2EE Component | Spring Boot Equivalent |
|----------------|------------------------|
| EJB Stateless Session Beans | Spring `@Service` with reactive return types (Mono/Flux) |
| EJB Stateful Session Beans | Spring service + Redis/DynamoDB for state |
| EJB Message-Driven Beans | Reactor Kafka / AWS SQS listeners |
| J2EE Security | Spring Security Reactive |
| J2EE Timer Service | Spring `@Scheduled` |
| JNDI DataSource | Spring `DataSource` bean / R2DBC |
| JMS | Amazon SQS / MSK (Kafka) |
| Work Manager / Async Beans | Reactor Schedulers |
| Application Server Clustering | ECS/EKS + ALB |
| Server Diagnostics | Spring Boot Actuator + CloudWatch |

### Data Access Migration

| J2EE JPA | Spring Data |
|----------|-------------|
| JPA with Hibernate/TopLink/EclipseLink | Spring Data R2DBC (reactive) |
| `persistence.xml` | `application.yml` R2DBC config |
| EntityManager | R2DatabaseClient |
| JPQL queries | Native SQL / query methods |
| JTA transactions | R2DBC reactive transactions |

### Messaging Migration

| J2EE JMS | AWS Messaging |
|----------|---------------|
| JMS Connection Factory | Kafka/SQS connection config |
| JMS Queues | Kafka topics / SQS queues |
| JMS Topics | Kafka topics / SNS topics |
| JMS MessageListener | Reactor Kafka / SQS async |
| XA Transactions | Saga pattern / Outbox pattern |

### Security Migration

| J2EE Security | Spring Security Reactive |
|---------------|--------------------------|
| User Registry (LDAP) | ReactiveAuthenticationManager |
| Security Tokens | JWT / OAuth2 |
| Security Roles | Spring authorities |
| `@RolesAllowed` | `@PreAuthorize` |
| Credential Vault | AWS Secrets Manager |

## Common Implementation Phases

### Phase 0: Dependency Analysis

1. Scan for J2EE imports (`javax.ejb`, `javax.servlet`, `javax.persistence`, `javax.jms`)
2. Identify application server-specific imports
3. Analyze deployment descriptors
4. Calculate dependency density scores
5. Generate migration complexity report

### Phase 1: Project Structure Migration

1. Update to Spring Boot 3.x parent
2. Remove ALL J2EE and application server dependencies
3. Add Spring Boot reactive starters:
   - `spring-boot-starter-webflux` (NOT `spring-boot-starter-web`)
   - `spring-boot-starter-data-r2dbc`
   - `spring-boot-starter-rsocket`
4. Configure multi-architecture Docker build (x86_64 + ARM64)

### Phase 2: Configuration Migration

1. Remove `web.xml` entirely
2. Migrate deployment descriptors to `application.yml`
3. Replace JNDI lookups with Spring DI
4. Configure R2DBC data sources

### Phase 3: EJB Migration

1. Convert Stateless Session Beans to `@Service`
2. Convert Stateful Session Beans to services + Redis
3. Migrate MDBs to reactive message listeners
4. Replace `@EJB` with constructor injection

### Phase 4: Data Access Migration

1. Remove `persistence.xml`
2. Configure Spring Data R2DBC
3. Convert JPA entities to R2DBC entities
4. Rewrite JPQL to native SQL

### Phase 5: Web Services Migration

1. Convert JAX-RS to Spring WebFlux
2. Replace servlet filters with WebFilter
3. Eliminate HttpServletRequest/Response usage

### Phase 6: Messaging Migration

1. Replace JMS with Kafka/SQS
2. Convert JMS producers to reactive publishers
3. Migrate MDBs to reactive consumers

### Phase 7: Security Migration

1. Replace J2EE security with Spring Security Reactive
2. Migrate user registries to Cognito/LDAP
3. Replace security tokens with JWT/OAuth2

### Phase 8: Container Optimization

1. Create multi-arch Dockerfile (x86_64 + ARM64)
2. Configure for AWS Java Runtime (Corretto)
3. Optimize for Graviton processors

## J2EE to Jakarta EE Namespace Change

All J2EE migrations must handle the namespace change:
- `javax.*` packages → `jakarta.*` packages
- Spring Boot 3.x uses Jakarta EE 9+
- Requires dependency updates across the board

## Common Code Migration Examples

### EJB to Spring Service

**Before (J2EE EJB):**
```java
@Stateless
public class OrderServiceBean implements OrderService {
    @Resource
    private SessionContext ctx;
    
    @EJB
    private InventoryService inventory;
    
    @TransactionAttribute(TransactionAttributeType.REQUIRED)
    public Order createOrder(OrderRequest request) {
        // blocking implementation
    }
}
```

**After (Spring Boot Reactive):**
```java
@Service
public class OrderService {
    private final InventoryService inventory;
    
    public OrderService(InventoryService inventory) {
        this.inventory = inventory;
    }
    
    @Transactional
    public Mono<Order> createOrder(OrderRequest request) {
        return inventory.checkStock(request.getItems())
            .flatMap(available -> saveOrder(request));
    }
}
```

### JMS MDB to Reactive Kafka

**Before (J2EE MDB):**
```java
@MessageDriven(activationConfig = {
    @ActivationConfigProperty(propertyName = "destinationType", 
                              propertyValue = "javax.jms.Queue"),
    @ActivationConfigProperty(propertyName = "destination", 
                              propertyValue = "jms/OrderQueue")
})
public class OrderMessageBean implements MessageListener {
    public void onMessage(Message message) {
        // blocking processing
    }
}
```

**After (Reactor Kafka):**
```java
@Component
public class OrderMessageConsumer {
    @Bean
    public Consumer<Flux<ReceiverRecord<String, Order>>> orderConsumer() {
        return records -> records
            .flatMap(record -> processOrder(record.value())
                .doOnSuccess(v -> record.receiverOffset().acknowledge()))
            .subscribe();
    }
}
```

### JAX-RS to WebFlux

**Before (JAX-RS):**
```java
@Path("/orders")
public class OrderResource {
    @GET
    @Path("/{id}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getOrder(@PathParam("id") String id) {
        Order order = orderService.findById(id);
        return Response.ok(order).build();
    }
}
```

**After (Spring WebFlux):**
```java
@RestController
@RequestMapping("/orders")
public class OrderController {
    private final OrderService orderService;
    
    @GetMapping("/{id}")
    public Mono<Order> getOrder(@PathVariable String id) {
        return orderService.findById(id);
    }
}
```

### JPA to R2DBC

**Before (JPA):**
```java
@Entity
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @OneToMany(mappedBy = "order", fetch = FetchType.LAZY)
    private List<OrderItem> items;
}

public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByCustomerId(Long customerId);
}
```

**After (R2DBC):**
```java
@Table("orders")
public class Order {
    @Id
    private Long id;
    // Note: No relationship annotations in R2DBC
}

public interface OrderRepository extends ReactiveCrudRepository<Order, Long> {
    Flux<Order> findByCustomerId(Long customerId);
}
```

## AWS Target Services

| Component | AWS Service |
|-----------|-------------|
| Container Orchestration | Amazon ECS / EKS |
| Database | Amazon Aurora PostgreSQL (R2DBC) |
| Messaging | Amazon SQS / MSK (Kafka) |
| Identity | Amazon Cognito |
| Caching | Amazon ElastiCache (Redis) |
| Secrets | AWS Secrets Manager |
| Configuration | AWS Parameter Store |
| Logging | Amazon CloudWatch Logs |
| Tracing | AWS X-Ray |
| Load Balancing | Application Load Balancer |

## Validation Criteria

All J2EE to Spring Boot reactive migrations must meet:

1. Zero J2EE/Jakarta/Application Server dependencies in final build
2. Application starts with embedded Netty (not servlet container)
3. All EJBs converted to Spring reactive services
4. All data access migrated to R2DBC
5. Messaging works with Kafka/SQS
6. Security implemented with Spring Security Reactive
7. Container runs on both x86_64 and ARM64 (Graviton)
8. All tests pass with WebTestClient and StepVerifier

## Risk Mitigation Patterns

### Stateful Session Bean State Management

**Risk**: Loss of conversational state
**Mitigation**: External session storage with Redis
```java
@Service
public class SessionStateService {
    private final ReactiveRedisTemplate<String, SessionState> redisTemplate;
    
    public Mono<SessionState> getState(String sessionId) {
        return redisTemplate.opsForValue().get(sessionId);
    }
    
    public Mono<Boolean> saveState(String sessionId, SessionState state) {
        return redisTemplate.opsForValue().set(sessionId, state, Duration.ofMinutes(30));
    }
}
```

### XA Transaction Replacement

**Risk**: Loss of distributed transaction support
**Mitigation**: Saga pattern with outbox
```java
@Service
public class OrderSagaService {
    public Mono<Order> createOrderSaga(OrderRequest request) {
        return orderRepository.save(order)
            .flatMap(saved -> outboxRepository.save(new OutboxEvent(saved)))
            .flatMap(event -> inventoryService.reserve(request.getItems())
                .onErrorResume(e -> compensate(order)));
    }
}
```

### Lazy Loading Replacement

**Risk**: N+1 query problems without lazy loading
**Mitigation**: Explicit reactive data fetching
```java
public Mono<OrderWithItems> getOrderWithItems(Long orderId) {
    return Mono.zip(
        orderRepository.findById(orderId),
        orderItemRepository.findByOrderId(orderId).collectList()
    ).map(tuple -> new OrderWithItems(tuple.getT1(), tuple.getT2()));
}
```
