# Marketplace 

 

## Scope of the system
The Marketplace system will allow general users to open a store to sell products or services. The system will act as a central hub for matching buyers and sellers.
## System users
System users are divided into two categories:
Buyers: Those who want to buy products or services.
Sellers: Those who want to sell products or services.
## System features
The Marketplace system has the following features:
- User registration and login
- Shopping cart system
- Product and service ordering
- Order creation and cancellation
- Store creation
- Address editing
- Subscription and store opening for sellers
- Product and service information management
- Product category management
- Price and sales condition setting
- Import and export record viewing
- Order viewing and status management
## Additional details
Developed using Django, Django REST Framework, and Vue.js
Still under development, but partially functional
Code available on GitHub
## Conclusion
The Marketplace system is a platform that connects buyers and sellers, providing features for transactions, order management, and store management. It's still under development, but has the potential to be a valuable resource for both parties.

## Entity Relations Diagram (ERD)
```mermaid

erDiagram 



User {
    id int PK
    username char UK
    password char 
    first_name char 
    last_name char
}

Customer {
    id int PK
    user int FK
    code char UK
    contact char 
    tel char
    fax char
    email char
    remark char
    province char
    district char
    sub_district char
    address char
    zip char
   
}

Shop {
    id int PK
    user int FK
    area int FK
    product_type int FK
    code char 
    name char
    contact char
    tel char
    fax char
    email char
    remark char
    province char
    district char
    sub_district char
    address char
    zip char

}


ProductType {
    id int PK
    name char
    count char 
    created_at  timestamp
    updated_at timestamp
}

Area {
    id int PK
    code char UK
    name char
    count int
}

Category {
    id int PK
    shop int FK
    name char
    count int
}

Product {
    id int PK
    shop int FK
    category int FK
    code char UK
    name char
    desc char
    unit int
    cost decimal
    price decimal
}

InputInvoice {
    id int PK
    shop int FK
    invoice_no char 
    type int 
    remark char
}

InputData {
    id int PK
    invoice int FK
    product int FK
    quantity  int 
    unit_price decimal
}

Cart {
    id int PK
    customer int FK
}

CartItem {
    id int PK 
    product int FK 
    unit int 
}

OutputInvoice {
    id int PK
    shop int FK 
    customer int FK
    invoice_no char
    remark char
    created_at  timestamp
    updated_at timestamp
}

OutputData {
    id int PK
    invoice int FK
    product int FK
    quantity int 
    unit_price decimal
}

Order {
    customer int PK
    shop int FK
    order_code char
    order_status int
    created_at  timestamp
    updated_at timestamp
}

OrderItem {
    order int PK
    product int FK
    unit int 
}

User ||--|| Shop : has 
User ||--|| Customer : has

Shop ||--|| Area : has 
Shop ||--|{ Product : have
Shop ||--|{ Category : have
Shop ||--|{ Order : have
Shop ||--|{ InputInvoice : have
Shop ||--|{ OutputInvoice : have

InputInvoice ||--|{ InputData : have
InputData ||--|| Product : has

Customer ||--|{ OutputInvoice : have
Customer ||--|{ Order : have
Customer ||--|| Cart : has

Cart ||--|{ CartItem : have
CartItem ||--|| Product :"has"

OutputInvoice ||--|{ OutputData : have
OutputData ||--|| Product : has

Product ||--|| Category : has
ProductType ||--|{ Shop : have

Order ||--|{ OrderItem : have
OrderItem ||--|| Product : has



```

---
## Data Dictionary

### User
| Field | Type  | Domain  |  Key |
|  ---  |  ---  |   ---   |  --- |
| id  | INT | 11 | PK |
| username | CHAR  |  (255) |
| email  | CHAR   | (255)  |
| password  | CHAR  |  (255) |

### ProductType
| Field | Type  | Domain  |  Key |
|  ---  |  ---  |   ---   |  --- |
| id  | INT | 11 | PK |   |
| name | CHAR  |  (255) |  |
| count  | INT  |  (255) |  |

### Area
| Field | Type  | Domain  |  Key |
|  ---  |  ---  |   ---   |  --- |
| id  | INT | 11 | PK |   |
| code | CHAR  |  (255) | UK |
| name | CHAR  |  (255) |  |
| count  | INT  |  (255) |  |



### Shop

| Field | Type  | Domain  |  Key |
|  ---  | ---   |  ---    |  --- |
| id  | INT | 11 | PK |   |
| user | INT  |  (11) |  FK |
| product_type | INT  |  (11) |  FK |
| area  | INT  |  (11) |  FK  |
| name  | CHAR   | (255)  | -    |
| code  | CHAR   | (6)  |  -   |
| contact  | CHAR   | (255)  |  -   |
| tel  | CHAR   | (10)  |  -   |
| fax  | CHAR   | (10)  |  -   |
| email  | CHAR   | (255)  |   -  |
| remark  | TEXT   | ()  | -    |
| address  | TEXT   | ()  | -    |
| province  | CHAR   | (255)  |   -  |
| district  | CHAR   | (255)  |   -  |
| sub_district  | CHAR   | (255)  |  -   |
| zip  | CHAR   | (5)  |   -  |
| created_at  | TIMESTAMP   | ()  |   -  |
| updated_at  | TIMESTAMP   | ()  |   -  |


### ProductCategory
| Field | Type  | Domain  |  Key |
|  ---  |  ---  |   ---   |  --- |
| id  | INT | 11 | PK |   |
| shop | INT  |  (11) | FK |
| name | CHAR  |  (255) | - |
| count  | INT  |  (11) | - |

### Product
| Field | Type  | Domain  |  Key |
|  ---  |  ---  |   ---   |  --- |
| id  | INT | 11 | PK |   |
| shop | INT  |  (11) | FK |
| category | INT  |  (11) | FK |
| code | CHAR  |  (8) | - |
| name | CHAR  |  (255) | - |
| desc | TEXT  |  () | - |
| unit | INT  |  (11) | - |
| price  | DECIMAL   | (9, 2)  | -    |
| cost  | DECIMAL   | (9, 2)  |  -   |
| created_at  | TIMESTAMP   | ()  |   -  |
| updated_at  | TIMESTAMP   | ()  |   -  |


### InputInvoice
| Field | Type  | Domain  |  Key |
|  ---  |  ---  |   ---   |  --- |
| id  | INT | 11 | PK |   |
| shop | INT  |  (11) | FK |
| invoice_no  | INT  |  (16) | - |
| type  | INT  |  (11) | - |
| remark  | TEXT   | ()  |  -   |
| created_at  | TIMESTAMP   | ()  |  -   |
| updated_at  | TIMESTAMP   | ()  |   -  |


### InputData
| Field | Type  | Domain  |  Key |
|  ---  |  ---  |   ---   |  --- |
| id  | INT | 11 | PK |   |
| shop | INT  |  (11) | FK |
| invoice  | INT  |  (11) | FK |
| quantity  | INT   | (11)  |   -  |
| unit_price  | DECIMAL   | (9, 2)  |   -  |
| created_at  | TIMESTAMP   | ()  |   -  |
| updated_at  | TIMESTAMP   | ()  |    - |


### Customer
| Field | Type  | Domain  |  Key |
|  ---  |  ---  |   ---   |  --- |
| id |   INT  |    (11)  |    PK   |
| user |  INT   |   (11)   |   FK    |
| code |   CHAR  |  (16)    |  FK     |
| contact |  CHAR   |  (255)    |    -   |
| tel |   CHAR  |   (10)   |    -   |
| fax |   CHAR  |    (10)  | -      |
| email |   CHAR  |    (255)  |   -    |
| remark |  TEXT   |   ()   |   -    |
| province |  CHAR   |  (255)    |   -    |
| district |   CHAR  |  (255)    |   -    |
| sub_district |   CHAR  |   (255)   |     -  |
| address |   TEXT  |   ()   |     -  |
| zip |  CHAR   |  (5)    |    -  |
| created_at |  TIMESTAMP   |  ()    |   -    |
| updated_at | TIMESTAMP    | ()     |    -   |


### Cart
| Field | Type  | Domain  |  Key |
|  ---  |  ---  |   ---   |  --- |
| id | INT | (11) | PK |
| customer | INT | (11) | FK |

### CartItem
| Field | Type  | Domain  |  Key |
|  ---  |  ---  |   ---   |  --- |
| id | INT | (11) | PK |
| cart | INT | (11)  |  FK  |
| product | INT | (11)  |  FK  |
| unit | INT | (11)  |  -  |


### Order
| Field | Type  | Domain  |  Key |
|  ---  |  ---  |   ---   |  --- |
| id | INT | (11) | PK |
|  customer  |   INT  |   (11)   |  FK    |
|  shop  |  INT   |   (11)   |   FK   |
|  order_code  |  CHAR   |   (9)   |   -   |
|  order_status  | INT    |   (11)   |   -   |
| created_at |  TIMESTAMP   |  ()    |    -   |
| updated_at | TIMESTAMP    | ()     |    -   |


### OrderItem
| Field | Type  | Domain  |  Key |
|  ---  |  ---  |   ---   |  --- |
| id | INT | (11) | PK |
|  order  |  INT  | (11)  |  FK  |
|  product  |  INT  | (11)  |  FK  |
|  unit  |  INT  | (11)  |  -  |



### OutputInvoice
| Field | Type  | Domain  |  Key |
|  ---  |  ---  |   ---   |  --- |
| id | INT | (11) | PK |
|  shop  |   INT  |  (11)   |   FK |
|  customer  |   INT  |  (11)   |  FK  |
|  invoice_no  |   CHAR  |  (16)   |  -  |
|  remark  |   TEXT  |  ()   |  -  |
| created_at |  TIMESTAMP   |  ()    |   -    |
| updated_at | TIMESTAMP    | ()     |   -    |



### OutputData

| Field | Type  | Domain  |  Key |
|  ---  |  ---  |   ---   |  --- |
| id | INT | (11) | PK |
|  invoice  |  INT    | ( 11) |  FK    |
|  product  |   INT   | (11 ) |  FK    |
|  quantity  |    INT  | (11 ) | FK     |
|  unit_price  |  DECIMAL    | (9,2 ) |   -   |
 




## Interface
### หน้าหลัก
