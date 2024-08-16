# MicroBizKeeper

MicroBizKeeper is a mobile record-keeping system designed for micro businesses. The application provides features such as sales record management, expense tracking, inventory management, customer database, and reporting. The backend is built using Django, Django REST Framework, and gRPC for microservices communication.

## Project Structure

/micro_biz_keeper
│
├── /services
│ ├── /auth_service
│ │ ├── grpc_server.py
│ │ ├── /auth
│ │ ├── /grpc_pb
│ │ │ ├── auth.proto
│ │ │ ├── auth_pb2.py
│ │ │ ├── auth_pb2_grpc.py
│ │ ├── /tests
│ │ └── requirements.txt
│ ├── /sales_service
│ ├── /expense_service
│ ├── /inventory_service
│ ├── /customer_service
│ └── /report_service
│
├── /custom_auth
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ └── ...
├── /deployments
│ ├── /k8s
│ └── /docker
│
└── README.md


## Features

- **Sales Record Management**: Track and manage sales, including customer information and transaction details.
- **Expense Tracking**: Record and categorize business expenses.
- **Inventory Management**: Keep track of inventory levels, item details, and stock value.
- **Customer Database**: Store customer information and maintain sales history.
- **Reporting**: Generate daily, monthly, and custom reports on sales, expenses, and inventory.

## Tech Stack

- **Backend**: Django, Django REST Framework, gRPC, Python
- **Authentication**: JWT tokens with `rest_framework_simplejwt`
- **Database**: SQLite (for development), PostgreSQL (recommended for production)
- **Microservices**: Auth service, sales service, expense service, inventory service, customer service, and report service
- **Containerization**: Docker
- **Orchestration**: Kubernetes

## Setup Instructions

### Prerequisites

- Python 3.7+
- pip
- Docker (optional, for containerization)
- Kubernetes (optional, for orchestration)

### Installation

1. **Clone the repository:**

   ```bash
   git clone git@github.com:mango-tech-org/micro_biz_keeper.git
   cd micro_biz_keeper
   ```
