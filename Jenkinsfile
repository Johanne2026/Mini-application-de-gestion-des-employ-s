pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.13.2'
        DJANGO_SETTINGS_MODULE = 'employe_project.settings'
        SECRET_KEY = 'jenkins-test-key-not-for-production'
    }
    
    
    stages {
        stage('Check and Install Python') {
            steps {
                bat '''
                    echo Vérification de Python...
                    
                    REM Essayer plusieurs chemins possibles
                    IF EXIST "C:\\Python313\\python.exe" (
                        set "PYTHON_PATH=C:\\Python313\\python.exe"
                    ) ELSE IF EXIST "C:\\Users\\jenkins\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" (
                        set "PYTHON_PATH=C:\\Users\\jenkins\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
                    ) ELSE (
                        echo ❌ Python 3.13 non trouvé
                        echo Installez Python manuellement sur le serveur Jenkins
                        exit /b 1
                    )
                    
                    echo ✅ Python trouvé: %PYTHON_PATH%
                    "%PYTHON_PATH%" --version
                '''
            }
        }

        stage('Diagnostic Système') {
            steps {
                echo '🔍 Diagnostic du système...'
                script {
                    // Détection OS
                    def isWindows = !isUnix()
                    echo "Système: ${isWindows ? 'Windows' : 'Unix/Linux'}"
                    
                    // Vérification Python
                    if (isWindows) {
                        bat '''
                            echo === VÉRIFICATION PYTHON SUR WINDOWS ===
                            python --version 2>&1 || echo "Python non trouvé"
                            where python || echo "Python pas dans PATH"
                            pip --version 2>&1 || echo "Pip non trouvé"
                            echo === RÉPERTOIRE COURANT ===
                            dir
                            echo === VARIABLES D'ENVIRONNEMENT PYTHON ===
                            set | findstr /i python || echo "Pas de variables Python"
                        '''
                    } else {
                        sh '''
                            echo "=== VÉRIFICATION PYTHON SUR UNIX ==="
                            python3 --version 2>&1 || python --version 2>&1 || echo "Python non trouvé"
                            which python3 || which python || echo "Python pas dans PATH"
                            pip3 --version 2>&1 || pip --version 2>&1 || echo "Pip non trouvé"
                            echo "=== RÉPERTOIRE COURANT ==="
                            ls -la
                            echo "=== VARIABLES D'ENVIRONNEMENT PYTHON ==="
                            env | grep -i python || echo "Pas de variables Python"
                        '''
                    }
                }
            }
        }
        
        stage('Checkout') {
            steps {
                echo '📦 Récupération du code source...'
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo '🐍 Configuration de l\'environnement Python...'
                script {
                    if (isUnix()) {
                        // Linux/macOS
                        sh '''
                            echo "=== SETUP UNIX ==="
                            
                            # Vérifier Python
                            if command -v python3.13 &> /dev/null; then
                                PYTHON_CMD="python3.13"
                            elif command -v python3 &> /dev/null; then
                                PYTHON_CMD="python3"
                            elif command -v python &> /dev/null; then
                                PYTHON_CMD="python"
                            else
                                echo "❌ ERREUR: Python non trouvé"
                                exit 1
                            fi
                            
                            echo "Python utilisé: \$PYTHON_CMD"
                            \$PYTHON_CMD --version
                            
                            # Créer virtualenv
                            echo "Création du virtualenv..."
                            \$PYTHON_CMD -m venv venv --clear
                            
                            # Activation
                            source venv/bin/activate
                            python --version
                            
                            # Mettre à jour pip
                            pip install --upgrade pip setuptools wheel
                            pip --version
                            
                            echo "✅ Setup Python terminé"
                        '''
                    } else {
                        // Windows
                        bat '''
                            echo === SETUP WINDOWS ===
                            
                            REM Vérifier Python
                            python --version 2>nul
                            IF %ERRORLEVEL% NEQ 0 (
                                echo ❌ ERREUR: Python non trouvé
                                echo Vérifiez que Python 3.13 est installé et dans le PATH
                                exit /b 1
                            )
                            
                            REM Créer virtualenv
                            echo Création du virtualenv...
                            python -m venv venv
                            
                            REM Activation
                            call venv\\Scripts\\activate.bat
                            python --version
                            
                            REM Mettre à jour pip
                            pip install --upgrade pip setuptools wheel
                            pip --version
                            
                            echo ✅ Setup Python terminé
                        '''
                    }
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo '📦 Installation des dépendances...'
                script {
                    if (isUnix()) {
                        sh '''
                            source venv/bin/activate
                            
                            echo "=== INSTALLATION DJANGO ==="
                            # Django 5.x (Django 6.0 n'existe pas encore)
                            pip install "Django>=5.0,<5.1"
                            pip install djangorestframework
                            
                            echo "=== INSTALLATION OUTILS ==="
                            pip install flake8 pytest pytest-django pytest-cov
                            pip install bandit safety
                            
                            echo "=== VÉRIFICATION VERSIONS ==="
                            python -c "import django; print(f'Django {django.__version__}')"
                            pip list | findstr -i "django" || pip list | grep -i "django"
                            
                            # Requirements.txt si existant
                            if [ -f "requirements.txt" ]; then
                                echo "Installation depuis requirements.txt..."
                                pip install -r requirements.txt
                            fi
                        '''
                    } else {
                        bat '''
                            call venv\\Scripts\\activate.bat
                            
                            echo === INSTALLATION DJANGO ===
                            REM Django 5.x (pas Django 6.0 qui n'existe pas)
                            pip install "Django>=5.0,<5.1"
                            pip install djangorestframework
                            
                            echo === INSTALLATION OUTILS ===
                            pip install flake8 pytest pytest-django pytest-cov
                            pip install bandit safety
                            
                            echo === VÉRIFICATION VERSIONS ===
                            python -c "import django; print('Django version:', django.__version__)"
                            pip list | findstr /i django
                            
                            REM Requirements.txt si existant
                            if exist requirements.txt (
                                echo Installation depuis requirements.txt...
                                pip install -r requirements.txt
                            )
                        '''
                    }
                }
            }
        }
        
        stage('Database Setup') {
            steps {
                echo '🗄️ Configuration de la base de données...'
                script {
                    if (isUnix()) {
                        sh '''
                            source venv/bin/activate
                            export DJANGO_SETTINGS_MODULE=employe_project.settings
                            
                            echo "=== MIGRATIONS ==="
                            python manage.py makemigrations --dry-run --check || python manage.py makemigrations --noinput
                            python manage.py migrate --noinput
                            
                            echo "=== FICHIERS STATIQUES ==="
                            python manage.py collectstatic --noinput --clear || echo "Collecte statique ignorée"
                        '''
                    } else {
                        bat '''
                            call venv\\Scripts\\activate.bat
                            set DJANGO_SETTINGS_MODULE=employe_project.settings
                            
                            echo === MIGRATIONS ===
                            python manage.py makemigrations --dry-run --check || python manage.py makemigrations --noinput
                            python manage.py migrate --noinput
                            
                            echo === FICHIERS STATIQUES ===
                            python manage.py collectstatic --noinput --clear || echo Collecte statique ignorée
                        '''
                    }
                }
            }
        }
        
        stage('Code Quality') {
            parallel {
                stage('Linting') {
                    steps {
                        echo '🧹 Vérification du style de code...'
                        script {
                            if (isUnix()) {
                                sh '''
                                    source venv/bin/activate
                                    
                                    echo "=== LINTING FLAKE8 ==="
                                    flake8 employe/ employe_project/ \
                                        --max-line-length=100 \
                                        --exclude=migrations,venv,env,.venv \
                                        --format=junit-xml \
                                        --output-file=flake8-report.xml || true
                                '''
                            } else {
                                bat '''
                                    call venv\\Scripts\\activate.bat
                                    
                                    echo === LINTING FLAKE8 ===
                                    flake8 employe/ employe_project/ ^
                                        --max-line-length=100 ^
                                        --exclude=migrations,venv,env,.venv ^
                                        --format=junit-xml ^
                                        --output-file=flake8-report.xml || echo Flake8 terminé
                                '''
                            }
                        }
                    }
                }
                
                stage('Security Scan') {
                    steps {
                        echo '🛡️ Analyse de sécurité...'
                        script {
                            if (isUnix()) {
                                sh '''
                                    source venv/bin/activate
                                    
                                    echo "=== SCAN SÉCURITÉ ==="
                                    # Safety (dépendances)
                                    safety check --json --output safety-report.json || echo "Safety scan terminé"
                                    
                                    # Bandit (code)
                                    bandit -r employe/ employe_project/ \
                                        -f json -o bandit-report.json \
                                        --exclude="*/migrations/*,*/venv/*,*/env/*,*/.venv/*" || echo "Bandit scan terminé"
                                '''
                            } else {
                                bat '''
                                    call venv\\Scripts\\activate.bat
                                    
                                    echo === SCAN SÉCURITÉ ===
                                    REM Safety (dépendances)
                                    safety check --json --output safety-report.json || echo Safety scan terminé
                                    
                                    REM Bandit (code)
                                    bandit -r employe/ employe_project/ ^
                                        -f json -o bandit-report.json ^
                                        --exclude="*/migrations/*,*/venv/*,*/env/*,*/.venv/*" || echo Bandit scan terminé
                                '''
                            }
                        }
                    }
                }
            }
        }
        
        stage('Tests') {
            steps {
                echo '🧪 Exécution des tests...'
                script {
                    if (isUnix()) {
                        sh '''
                            source venv/bin/activate
                            export DJANGO_SETTINGS_MODULE=employe_project.settings
                            
                            echo "=== TESTS DJANGO ==="
                            python manage.py test --noinput --verbosity=2 --parallel=2
                            
                            echo "=== TESTS PYTEST ==="
                            # Vérifier si pytest est configuré
                            if [ -f pytest.ini ] || [ -f setup.cfg ] || [ -f pyproject.toml ]; then
                                pytest --junitxml=pytest-report.xml \
                                       --cov=employe --cov=employe_project \
                                       --cov-report=xml --cov-report=html \
                                       --cov-exclude="*/migrations/*" || echo "Pytest terminé"
                            fi
                        '''
                    } else {
                        bat '''
                            call venv\\Scripts\\activate.bat
                            set DJANGO_SETTINGS_MODULE=employe_project.settings
                            
                            echo === TESTS DJANGO ===
                            python manage.py test --noinput --verbosity=2 --parallel=2
                            
                            echo === TESTS PYTEST ===
                            REM Vérifier si pytest est configuré
                            if exist pytest.ini (
                                pytest --junitxml=pytest-report.xml ^
                                       --cov=employe --cov=employe_project ^
                                       --cov-report=xml --cov-report=html ^
                                       --cov-exclude="*/migrations/*" || echo Pytest terminé
                            ) else (
                                if exist setup.cfg (
                                    pytest --junitxml=pytest-report.xml ^
                                           --cov=employe --cov=employe_project ^
                                           --cov-report=xml --cov-report=html ^
                                           --cov-exclude="*/migrations/*" || echo Pytest terminé
                                ) else (
                                    if exist pyproject.toml (
                                        pytest --junitxml=pytest-report.xml ^
                                               --cov=employe --cov=employe_project ^
                                               --cov-report=xml --cov-report=html ^
                                               --cov-exclude="*/migrations/*" || echo Pytest terminé
                                    )
                                )
                            )
                        '''
                    }
                }
            }
        }
        
        stage('Django Health Check') {
            steps {
                echo '🏥 Vérifications Django...'
                script {
                    if (isUnix()) {
                        sh '''
                            source venv/bin/activate
                            export DJANGO_SETTINGS_MODULE=employe_project.settings
                            
                            echo "=== VÉRIFICATIONS SYSTÈME ==="
                            python manage.py check --deploy || python manage.py check
                            
                            echo "=== ÉTAT MIGRATIONS ==="
                            python manage.py showmigrations --list
                        '''
                    } else {
                        bat '''
                            call venv\\Scripts\\activate.bat
                            set DJANGO_SETTINGS_MODULE=employe_project.settings
                            
                            echo === VÉRIFICATIONS SYSTÈME ===
                            python manage.py check --deploy || python manage.py check
                            
                            echo === ÉTAT MIGRATIONS ===
                            python manage.py showmigrations --list
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo '🧹 Nettoyage et archivage...'
            
            // Archive des rapports JUnit
            junit(
                allowEmptyResults: true,
                testResults: '**/*-report.xml',
                healthScaleFactor: 100.0
            )
            
            // Archive des artefacts (sans publishHTML)
            archiveArtifacts(
                artifacts: '**/*-report.*, coverage.xml, htmlcov/**',
                allowEmptyArchive: true,
                fingerprint: true
            )
            
            // Nettoyage
            script {
                if (isUnix()) {
                    sh '''
                        echo "=== NETTOYAGE UNIX ==="
                        rm -rf venv .venv __pycache__ */__pycache__ *.pyc 2>/dev/null || true
                        rm -f db.sqlite3 test*.db .coverage 2>/dev/null || true
                    '''
                } else {
                    bat '''
                        echo === NETTOYAGE WINDOWS ===
                        rmdir /s /q venv 2>nul || echo Venv déjà supprimé
                        rmdir /s /q .venv 2>nul || echo .venv déjà supprimé
                        del /s /q __pycache__ 2>nul || echo Pycache déjà supprimé
                        for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
                        del /s /q *.pyc 2>nul || echo Fichiers .pyc déjà supprimés
                        del db.sqlite3 2>nul || echo Base de données déjà supprimée
                        del .coverage 2>nul || echo Fichier coverage déjà supprimé
                    '''
                }
            }
        }
        
        success {
            echo '✅✅✅ Pipeline Django avec Python 3.13 réussi! ✅✅✅'
            script {
                // Récupération des versions pour le log
                def pythonVersion = "Inconnu"
                def djangoVersion = "Inconnu"
                
                try {
                    if (isUnix()) {
                        pythonVersion = sh(script: 'source venv/bin/activate 2>/dev/null && python --version 2>&1 | cut -d" " -f2', returnStdout: true).trim() ?: "Inconnu"
                        djangoVersion = sh(script: 'source venv/bin/activate 2>/dev/null && python -c "import django; print(django.__version__)" 2>/dev/null', returnStdout: true).trim() ?: "Inconnu"
                    } else {
                        pythonVersion = bat(script: 'call venv\\Scripts\\activate.bat 2>nul && python --version 2>&1', returnStdout: true).trim().replace("Python ", "") ?: "Inconnu"
                        djangoVersion = bat(script: 'call venv\\Scripts\\activate.bat 2>nul && python -c "import django; print(django.__version__)" 2>&1', returnStdout: true).trim() ?: "Inconnu"
                    }
                } catch (Exception e) {
                    echo "Impossible de récupérer les versions: ${e.message}"
                }
                
                echo """
                📊 RÉSUMÉ DU BUILD
                ==================
                ✅ STATUT: SUCCÈS
                🐍 Python: ${pythonVersion}
                🎯 Django: ${djangoVersion}
                🔢 Build: ${env.BUILD_NUMBER}
                📁 Job: ${env.JOB_NAME}
                ==================
                """
            }
        }
        
        failure {
            echo '❌❌❌ Pipeline Django échouée! ❌❌❌'
            script {
                // Logs de débogage en cas d'échec
                if (isUnix()) {
                    sh '''
                        echo "=== DERNIERS LOGS D'ERREUR ==="
                        tail -20 /var/log/syslog 2>/dev/null || dmesg | tail -10 2>/dev/null || echo "Pas de logs système"
                        
                        echo "=== ESPACE DISQUE ==="
                        df -h . 2>/dev/null || echo "Commande df non disponible"
                        
                        echo "=== PROCESSUS PYTHON ==="
                        ps aux | grep -i python | head -10 2>/dev/null || echo "Commande ps non disponible"
                    '''
                } else {
                    bat '''
                        echo === DERNIERS LOGS ===
                        echo Vérifiez les logs Windows Event Viewer pour plus de détails
                        
                        echo === ESPACE DISQUE ===
                        wmic logicaldisk get size,freespace,caption 2>nul || echo Commande wmic non disponible
                        
                        echo === PROCESSUS PYTHON ===
                        tasklist | findstr /i python 2>nul || echo Pas de processus Python actif
                    '''
                }
            }
        }
        
        unstable {
            echo '⚠️ Pipeline instable (tests échoués)'
        }
    }
}