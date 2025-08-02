#!/bin/bash

# LoyalLight MVP Launch Script
# Automated setup and launch script for the LoyalLight MVP application
# This script handles dependency installation and service startup

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ASCII Art Banner
echo -e "${PURPLE}"
echo "██╗      ██████╗ ██╗   ██╗ █████╗ ██╗     ██╗     ██╗ ██████╗ ██╗  ██╗████████╗"
echo "██║     ██╔═══██╗╚██╗ ██╔╝██╔══██╗██║     ██║     ██║██╔════╝ ██║  ██║╚══██╔══╝"
echo "██║     ██║   ██║ ╚████╔╝ ███████║██║     ██║     ██║██║  ███╗███████║   ██║   "
echo "██║     ██║   ██║  ╚██╔╝  ██╔══██║██║     ██║     ██║██║   ██║██╔══██║   ██║   "
echo "███████╗╚██████╔╝   ██║   ██║  ██║███████╗███████╗██║╚██████╔╝██║  ██║   ██║   "
echo "╚══════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   "
echo -e "${NC}"
echo -e "${CYAN}🚀 LoyalLight MVP - Automated Setup & Launch Script${NC}"
echo -e "${CYAN}===============================================${NC}"
echo ""

# Function to print status messages
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check and install dependencies
check_dependencies() {
    print_status "Checking system dependencies..."
    
    # Check Python
    if ! command_exists python3; then
        print_error "Python 3 is not installed. Please install Python 3.11+ and try again."
        exit 1
    fi
    
    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_success "Python $python_version found"
    
    # Check Node.js
    if ! command_exists node; then
        print_error "Node.js is not installed. Please install Node.js 16+ and try again."
        exit 1
    fi
    
    node_version=$(node --version)
    print_success "Node.js $node_version found"
    
    # Check Yarn
    if ! command_exists yarn; then
        print_warning "Yarn not found. Installing yarn..."
        npm install -g yarn
    fi
    
    yarn_version=$(yarn --version)
    print_success "Yarn $yarn_version found"
    
    # Check if MongoDB is accessible (optional)
    print_status "MongoDB connection will be tested when starting the backend..."
}

# Function to setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    # Navigate to backend directory
    cd backend || { print_error "Backend directory not found"; exit 1; }
    
    # Create virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv .venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source .venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating default .env file..."
        cat > .env << EOF
MONGO_URL=mongodb://localhost:27017
DB_NAME=loyallight_mvp
DEBUG=false
EOF
        print_warning "Please review and update the .env file with your MongoDB connection details."
    fi
    
    cd ..
    print_success "Backend setup completed"
}

# Function to setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    # Navigate to frontend directory
    cd frontend || { print_error "Frontend directory not found"; exit 1; }
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    yarn install
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating default .env file..."
        cat > .env << EOF
REACT_APP_BACKEND_URL=http://localhost:8001
WDS_SOCKET_PORT=3000
EOF
        print_warning "Please review and update the .env file with your backend URL."
    fi
    
    cd ..
    print_success "Frontend setup completed"
}

# Function to start services
start_services() {
    print_status "Starting LoyalLight MVP services..."
    
    # Create logs directory
    mkdir -p logs
    
    # Start backend
    print_status "Starting backend server..."
    cd backend
    source .venv/bin/activate
    nohup uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload > ../logs/backend.log 2>&1 &
    backend_pid=$!
    echo $backend_pid > ../logs/backend.pid
    cd ..
    
    # Wait a moment for backend to start
    sleep 3
    
    # Check if backend is running
    if ps -p $backend_pid > /dev/null; then
        print_success "Backend server started (PID: $backend_pid)"
        print_status "Backend available at: http://localhost:8001"
        print_status "API documentation: http://localhost:8001/docs"
    else
        print_error "Failed to start backend server. Check logs/backend.log for details."
        exit 1
    fi
    
    # Start frontend
    print_status "Starting frontend development server..."
    cd frontend
    nohup yarn start > ../logs/frontend.log 2>&1 &
    frontend_pid=$!
    echo $frontend_pid > ../logs/frontend.pid
    cd ..
    
    # Wait a moment for frontend to start
    sleep 5
    
    # Check if frontend is running
    if ps -p $frontend_pid > /dev/null; then
        print_success "Frontend server started (PID: $frontend_pid)"
        print_status "Frontend available at: http://localhost:3000"
    else
        print_error "Failed to start frontend server. Check logs/frontend.log for details."
        exit 1
    fi
}

# Function to show running services status
show_status() {
    echo ""
    echo -e "${CYAN}🌟 LoyalLight MVP is now running!${NC}"
    echo -e "${CYAN}=================================${NC}"
    echo ""
    echo -e "${GREEN}Backend Services:${NC}"
    echo -e "  • API Server: ${BLUE}http://localhost:8001${NC}"
    echo -e "  • API Documentation: ${BLUE}http://localhost:8001/docs${NC}"
    echo -e "  • Interactive API: ${BLUE}http://localhost:8001/redoc${NC}"
    echo ""
    echo -e "${GREEN}Frontend Services:${NC}"
    echo -e "  • Web Application: ${BLUE}http://localhost:3000${NC}"
    echo ""
    echo -e "${GREEN}Logs:${NC}"
    echo -e "  • Backend logs: ${YELLOW}logs/backend.log${NC}"
    echo -e "  • Frontend logs: ${YELLOW}logs/frontend.log${NC}"
    echo ""
    echo -e "${GREEN}Management:${NC}"
    echo -e "  • Stop services: ${YELLOW}./stop_mvp.sh${NC}"
    echo -e "  • View logs: ${YELLOW}tail -f logs/*.log${NC}"
    echo ""
}

# Function to create stop script
create_stop_script() {
    cat > stop_mvp.sh << 'EOF'
#!/bin/bash

# LoyalLight MVP Stop Script

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Stopping LoyalLight MVP services...${NC}"

# Stop backend
if [ -f "logs/backend.pid" ]; then
    backend_pid=$(cat logs/backend.pid)
    if ps -p $backend_pid > /dev/null; then
        kill $backend_pid
        echo -e "${GREEN}Backend server stopped${NC}"
    fi
    rm -f logs/backend.pid
fi

# Stop frontend
if [ -f "logs/frontend.pid" ]; then
    frontend_pid=$(cat logs/frontend.pid)
    if ps -p $frontend_pid > /dev/null; then
        kill $frontend_pid
        echo -e "${GREEN}Frontend server stopped${NC}"
    fi
    rm -f logs/frontend.pid
fi

# Kill any remaining processes
pkill -f "uvicorn app.main:app"
pkill -f "yarn start"

echo -e "${GREEN}All LoyalLight MVP services stopped${NC}"
EOF

    chmod +x stop_mvp.sh
    print_success "Stop script created: ./stop_mvp.sh"
}

# Main execution
main() {
    # Check if we're in the right directory
    if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
        print_error "Please run this script from the LoyalLight MVP root directory"
        exit 1
    fi
    
    # Parse command line arguments
    case "${1:-start}" in
        "setup")
            check_dependencies
            setup_backend
            setup_frontend
            print_success "Setup completed! Run './launch_mvp.sh start' to start services."
            ;;
        "start")
            check_dependencies
            setup_backend
            setup_frontend
            start_services
            create_stop_script
            show_status
            ;;
        "stop")
            if [ -f "stop_mvp.sh" ]; then
                ./stop_mvp.sh
            else
                print_error "Stop script not found. Services may not have been started with this script."
            fi
            ;;
        "status")
            if [ -f "logs/backend.pid" ] && [ -f "logs/frontend.pid" ]; then
                backend_pid=$(cat logs/backend.pid)
                frontend_pid=$(cat logs/frontend.pid)
                
                echo -e "${CYAN}Service Status:${NC}"
                
                if ps -p $backend_pid > /dev/null; then
                    echo -e "  Backend: ${GREEN}Running${NC} (PID: $backend_pid)"
                else
                    echo -e "  Backend: ${RED}Stopped${NC}"
                fi
                
                if ps -p $frontend_pid > /dev/null; then
                    echo -e "  Frontend: ${GREEN}Running${NC} (PID: $frontend_pid)"
                else
                    echo -e "  Frontend: ${RED}Stopped${NC}"
                fi
            else
                echo -e "${YELLOW}Services not started with this script${NC}"
            fi
            ;;
        "help"|"-h"|"--help")
            echo -e "${CYAN}LoyalLight MVP Launch Script${NC}"
            echo ""
            echo "Usage: $0 [command]"
            echo ""
            echo "Commands:"
            echo "  start   - Setup and start all services (default)"
            echo "  setup   - Only setup dependencies without starting"
            echo "  stop    - Stop all running services"
            echo "  status  - Show service status"
            echo "  help    - Show this help message"
            echo ""
            ;;
        *)
            print_error "Unknown command: $1"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"