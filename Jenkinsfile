pipeline {
    agent any
    
    environment {
        COMPOSE_FILE = 'docker-compose-jenkins.yml'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Fetching code from GitHub...'
                git branch: 'main',
                    url: 'https://github.com/fizaf0012/reddit-sentiment-analyzer.git'
            }
        }
        
        stage('Stop Existing Containers') {
            steps {
                echo 'Stopping any existing containers...'
                sh '''
                    docker-compose -f ${COMPOSE_FILE} down || true
                '''
            }
        }
        
        stage('Build and Deploy') {
            steps {
                echo 'Building and starting containers...'
                sh '''
                    docker-compose -f ${COMPOSE_FILE} up -d --build
                '''
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo 'Verifying containers are running...'
                sh '''
                    docker-compose -f ${COMPOSE_FILE} ps
                '''
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}