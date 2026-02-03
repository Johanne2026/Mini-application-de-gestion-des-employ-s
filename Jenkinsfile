pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        DJANGO_SETTINGS_MODULE = 'employe_project.settings'
        SECRET_KEY = 'jenkins-test-key-not-for-production'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Récupération du code source...'
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo 'Configuration de l\'environnement Python...'
                sh '''
                    python3 --version || python --version
                    python3 -m venv venv || python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install wheel setuptools
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installation des dépendances...'
                sh '''
                    . venv/bin/activate
                    # Installation des dépendances principales
                    pip install Django==6.0
                    pip install djangorestframework
                    
                    # Installation des outils de développement
                    pip install flake8 pytest pytest-django pytest-cov
                    pip install bandit safety
                    
                    # Si un requirements.txt existe, l'utiliser
                    if [ -f requirements.txt ]; then
                        pip install -r requirements.txt
                    fi
                '''
            }
        }
        
        stage('Database Setup') {
            steps {
                echo 'Configuration de la base de données...'
                sh '''
                    . venv/bin/activate
                    export DJANGO_SETTINGS_MODULE=employe_project.settings
                    
                    # Migrations
                    python manage.py makemigrations --dry-run --check || python manage.py makemigrations
                    python manage.py migrate --noinput
                    
                    # Collecte des fichiers statiques
                    python manage.py collectstatic --noinput --clear || true
                '''
            }
        }
        
        stage('Code Quality') {
            parallel {
                stage('Linting') {
                    steps {
                        echo 'Vérification du style de code...'
                        sh '''
                            . venv/bin/activate
                            flake8 employe/ employe_project/ --max-line-length=100 \
                                --exclude=migrations,venv,env \
                                --format=junit-xml --output-file=flake8-report.xml || true
                        '''
                    }
                }
                
                stage('Security Scan') {
                    steps {
                        echo 'Analyse de sécurité...'
                        sh '''
                            . venv/bin/activate
                            # Scan des dépendances
                            safety check --json --output safety-report.json || true
                            
                            # Scan du code Django
                            bandit -r employe/ employe_project/ \
                                -f json -o bandit-report.json \
                                --exclude="*/migrations/*,*/venv/*" || true
                        '''
                    }
                }
            }
        }
        
        stage('Tests') {
            steps {
                echo 'Exécution des tests...'
                sh '''
                    . venv/bin/activate
                    export DJANGO_SETTINGS_MODULE=employe_project.settings
                    
                    # Tests Django natifs
                    python manage.py test --noinput --verbosity=2
                    
                    # Tests avec pytest si configuré
                    if [ -f pytest.ini ] || [ -f setup.cfg ] || [ -f pyproject.toml ]; then
                        pytest --junitxml=pytest-report.xml \
                               --cov=employe --cov=employe_project \
                               --cov-report=xml --cov-report=html \
                               --cov-exclude="*/migrations/*" || true
                    fi
                '''
            }
        }
        
        stage('Django Check') {
            steps {
                echo 'Vérifications Django...'
                sh '''
                    . venv/bin/activate
                    export DJANGO_SETTINGS_MODULE=employe_project.settings
                    
                    # Vérifications système Django
                    python manage.py check --deploy || python manage.py check
                    
                    # Vérification des migrations
                    python manage.py showmigrations
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Nettoyage et archivage des résultats...'
            
            // Archive des rapports de tests
            junit(
                allowEmptyResults: true,
                testResults: '*-report.xml'
            )
            
            // Rapport de couverture
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report',
                reportTitles: ''
            ])
            
            // Archive des artefacts
            archiveArtifacts(
                artifacts: '**/*-report.json, **/*-report.xml, **/htmlcov/**',
                allowEmptyArchive: true
            )
            
            // Nettoyage
            sh '''
                rm -rf venv || true
                rm -f db.sqlite3 || true
            '''
        }
        
        success {
            echo '✅ Pipeline Django réussie!'
            // Optionnel: notification Slack/Teams
            // slackSend(channel: '#dev', message: "✅ Build réussi pour ${env.JOB_NAME} - ${env.BUILD_NUMBER}")
        }
        
        failure {
            echo '❌ Pipeline Django échouée!'
            // Optionnel: notification d'échec
            // slackSend(channel: '#dev', message: "❌ Build échoué pour ${env.JOB_NAME} - ${env.BUILD_NUMBER}")
        }
        
        unstable {
            echo '⚠️ Pipeline Django instable (tests échoués mais build OK)'
        }
    }
}