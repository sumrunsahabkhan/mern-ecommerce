pipeline {
    agent { label 'ubuntu3' }

    environment {
        DOCKER_NETWORK = 'ci-network'
    }

    stages {

        stage('Clone Main Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/sumrunsahabkhan/mern-ecommerce.git'
            }
        }

        stage('Build & Run Main Containers') {
            steps {
                sh '''
                sudo docker compose down || true
                sudo docker compose up -d --build
                '''
            }
        }

        stage('Verify Running Containers') {
            steps {
                sh 'sudo docker ps'
            }
        }

        stage('Wait for Frontend to Start') {
            steps {
                script {
                    sh '''
                    echo "Waiting for user-frontend-ci (5173) to be ready..."
                    while ! sudo docker run --rm --network=ci-network busybox nc -z user-frontend-ci 5173; do
                        echo "Frontend not ready... retrying..."
                        sleep 2
                    done
                    echo "Frontend is UP!"
                    '''
                }
            }
        }

        stage('Run Selenium Tests') {
            steps {
                dir('selenium-tests') {
                    sh '''
                    echo "Building Selenium Test Image..."
                    sudo docker build -t selenium-tests .
                    echo "Running Selenium Tests..."
                    sudo docker run --rm \
                        --network=ci-network \
                        -e BASE_URL="http://3.80.204.243:3005" \
                        selenium-tests
                    '''
                }
            }
        }

        stage('Show Logs') {
            steps {
                sh 'sudo docker compose logs --tail=100'
            }
        }
    }

    post {
        success {
            script {
                echo "✅ CI Build Completed Successfully!"
                mail (
                    subject: "Tests PASSED: ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                    body: "All tests passed.\nBuild: ${env.BUILD_URL}",
                    to: "sumrunk568@gmail.com,qasimalik@gmail.com"
                )
            }
        }
        failure {
            script {
                echo "❌ Build Failed. Check logs."
                mail (
                    subject: "Tests FAILED: ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                    body: "Tests failed.\nBuild: ${env.BUILD_URL}",
                    to: "sumrunk568@gmail.com,qasimalik@gmail.com"
                )
            }
        }
    }
}
