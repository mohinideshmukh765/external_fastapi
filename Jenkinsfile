pipeline {

    agent any

    stages {

        stage('Train ML Model') {
            steps {
                bat 'python train_model.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t fastapi-diabetes .'
            }
        }

        stage('Stop Old Container') {
            steps {
                bat '''
                docker stop fastapi-diabetes >nul 2>&1 || ver >nul
                docker rm fastapi-diabetes >nul 2>&1 || ver >nul
                '''
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker run -d -p 8083:8000 --name fastapi-diabetes fastapi-diabetes'
            }
        }

        stage('Verify Deployment') {
            steps {
                bat 'docker ps'
            }
        }
    }
}