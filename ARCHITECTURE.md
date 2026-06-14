# Technical Architecture

## 1. Repository Structure

The repository is divided into several main directories:

- **`frontend-client/`**: Contains the Angular frontend application code. It includes components, services, and routing for the web interface.
- **`server/`**: Contains the Python Flask backend application code. It serves API endpoints, communicates with the database, and orchestrates network sandbox tasks.
- **`device_bundles/`**: Contains modules specific to different network device types (e.g., VyOS). This is where device-specific interactions and configurations are defined.
- **`network/`**: Contains core network logic and utilities used by the server.
- **`testcases/`**: Contains definitions and configurations for network test cases.
- **`SandboxInternalTestController/`**: Contains scripts and utilities for internal sandbox testing.
- **`trigger_tests.py`**: A top-level Python script for triggering test runs.

## 2. Building and Running the Applications

### Frontend (Angular)

To run the frontend client:

1. Navigate to the frontend directory: `cd frontend-client`
2. Use the correct Node version: `nvm use`
3. Install dependencies (if you haven't already): `npm install`
4. Run the development server: `npm run start` (or `ng serve`)
5. The application will be accessible at `http://localhost:4200`.

### Backend (Flask)

To run the Python Flask backend:

1. Navigate to the root directory of the repository.
2. Install the required Python dependencies: `pip install -r requirements.txt`
3. Start the server as a Python module: `python -m server`
4. The backend API will be accessible, typically at `http://127.0.0.1:5000`.

## 3. Requirements

To successfully run and deploy the Network Deployment Tool, the following dependencies must be pre-installed and configured:

- **GNS3**: A network software emulator that must be installed and running. It is used to simulate the network topologies.
- **Docker**: Used for containerized applications and possibly for running specific node types within GNS3.
- **MongoDB**: A NoSQL database used to store application state, test results, and device configurations. 
  - *Setup*: Ensure MongoDB is running locally or accessible remotely. The backend will attempt to connect to it using the configured connection string.

## 4. How to Add a New Device Type

Adding support for a new network device type involves creating a new device bundle and ensuring compatibility with GNS3.

1. **Create a Device Bundle**:
   - In the `device_bundles/` directory, create a new folder named after your device type (e.g., `device_bundles/my_new_device/`).
   - **Implement the required contract**: Your new device bundle must provide connection modules (like API, SSH, Telnet) and encapsulate them in a `DeviceBundleConfig` instance. You MUST implement connections for all the following operations defined in the `Operation` enum: `DEPLOY_CONFIG`, `GET_RUNNING_CONFIG`, `CHECK_CONNECTION`, `SANDBOX_CONSOLE_CONFIG`, `NETWORK_MAPPING`, and `UNIT_TESTS`. You can find the base template and definitions in `device_bundles/base/bundle_config.py`.
   - **Registration**: The new bundle must be registered with the `BundleRegistry` (e.g., via `BundleRegistry.register(MY_BUNDLE)` in `bundle_config.py`). Also, ensure the new bundle is imported in `device_bundles/__init__.py` so it registers on startup.
   - **Naming Convention**: The `device_type` property configured in your bundle *must exactly match* the `deviceType` field of the device in the MongoDB database, otherwise the system will not be able to find the matching bundle.

2. **GNS3 Template Requirement**:
   - For the system to spawn and interact with the device in the emulator, a corresponding template must be defined in GNS3.
   - **Crucial**: The template defined in GNS3 must be named *exactly* correctly to match the identifier used by your new device bundle. If the names do not match, the backend will not be able to instruct GNS3 to spawn the correct node type.

## 5. Configuration (Environment Variables)

The application relies on several environment variables for configuration. If not set, it will fallback to the default values listed below:

### Server & Database
- **`FLASK_HOST`**: The host address for the Flask backend API. *(Default: `localhost`)*
- **`FLASK_PORT`**: The port number for the Flask backend API. *(Default: `5000`)*
- **`MONGODB_URI`**: The connection string for the MongoDB database. *(Default: `mongodb://localhost:27017/`)*
- **`ADMIN_USERNAME`**: The default admin username created during database initialization. *(Default: `admin`)*
- **`ADMIN_PASSWORD`**: The default admin password created during database initialization. *(Default: `admin1`)*

### Sandbox & Docker Connections
- **`SANDBOX_HOST`**: The host address for the Sandbox Internal Controller. *(Default: `localhost`)*
- **`SANDBOX_PORT`**: The port number for the Sandbox Internal Controller. *(Default: `5011`)*
- **`DOCKER_HOST`**: The remote Docker host used for running test containers. *(Default: `tcp://localhost:2375`)*

### GNS3 Connection
- **`GNS3_URL`**: The URL to the GNS3 server. *(Default: `http://localhost:3080`)*
- **`GNS3_USER`**: The username for GNS3 server authentication. *(Default: `admin`)*
- **`GNS3_PASSWORD`**: The password for GNS3 server authentication. *(Default: `admin`)*

## 6. Database Initialization and Deployment Configuration

The application stores essential configurations, credentials, and deployment lifecycle states in the MongoDB database. This state ensures that the pipeline correctly orchestrates the network sandbox without losing track of current deployment progress.

### Initialization Method

To populate the initial state (such as the default admin user, test cases, and deployment statuses), you should run the provided initialization script before starting the server for the first time:

```bash
python -m server.init_database
```

*(You can also pass the `--reset` flag to drop all existing collections and start fresh).*

### DeploymentStatus Configuration

The MongoDB database maintains a single `DeploymentStatus` document that orchestrates the sandbox operations. The initialization script automatically seeds this document with the following fields:

- **`Deployed`**: Tracks if the final network deployment has been successfully rolled out (Initial value: `"False"`).
- **`SyntaxTest`**: Tracks if the network configurations have passed syntax verification in the sandbox (Initial value: `"False"`).
- **`UnitTest`**: Tracks if the automated tests successfully ran against the sandbox environment (Initial value: `"False"`).
- **`AttachemendPoint`**: Specifies the subnet to link the internal test server to the GNS3 topology. *(Default: `"192.168.18.0/255.255.255.0"`)*
- **`ImageName`**: Specifies the Docker image name used to spawn the test server container. *(Default: `"sandbox-server"`)*
- **`SrvAddress`**: Specifies the internal IP address assigned to the Docker container when spun up. *(Default: `"10.0.0.2"`)*
- **`CurrentConfig`**: A reference to the currently active configurations stored in the `ConfigVersions` collection.
