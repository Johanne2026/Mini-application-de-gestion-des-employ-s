pipeline {
    agent any
    
    environment {
        // 🔥 Version Python à utiliser
        PYTHON_VERSION = '3.13'
        // Vérifier les chemins pour Python 3.13
        PYTHON_PATHS = "/usr/local/bin:/usr/bin:/opt/homebrew/bin:/usr/local/opt/python@3.13/bin"
        
        // Django
        DJANGO_SETTINGS_MODULE = 'employe_project.settings'
        SECRET_KEY = 'jenkins-test-key-not-for-production'
        
        // Mise à jour du PATH avec Python 3.13
        PATH = "${env.PYTHON_PATHS}:${env.PATH}"
        
        // Variables pip
        PIP_NO_CACHE_DIR = 'false'
        PIP_CACHE_DIR = '/tmp/pip-cache'
    }
    
    options {
        timeout(time: 30, unit: 'MINUTES')
        retry(2) // Réessayer en cas d'échec
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📦 Récupération du code source...'
                checkout scm
            }
        }
        
        stage('Diagnostic Système') {
            steps {
                echo '🔍 Diagnostic de l\'environnement...'
                sh '''
                    echo "=== PLATEFORME ==="
                    uname -a
                    lsb_release -a 2>/dev/null || cat /etc/*release 2>/dev/null || echo "Non disponible"
                    
                    echo "=== PYTHON DISPONIBLE ==="
                    echo "Recherche Python 3.13..."
                    find /usr -name "*python3.13*" 2>/dev/null | head -10 || echo "Non trouvé dans /usr"
                    find /usr/local -name "*python3.13*" 2>/dev/null | head -10 || echo "Non trouvé dans /usr/local"
                    find /opt -name "*python3.13*" 2>/dev/null | head -10 || echo "Non trouvé dans /opt"
                    
                    echo "=== VERSIONS INSTALLÉES ==="
                    ls -la /usr/bin/python* 2>/dev/null || true
                    ls -la /usr/local/bin/python* 2>/dev/null || true
                    ls -la /opt/homebrew/bin/python* 2>/dev/null || true
                    
                    echo "=== COMMANDES DISPONIBLES ==="
                    command -v python3.13 && echo "✓ python3.13 disponible" || echo "✗ python3.13 non trouvé"
                    command -v python3 && python3 --version || echo "python3 non disponible"
                    command -v python && python --version || echo "python non disponible"
                    
                    echo "=== PATH ACTUEL ==="
                    echo $PATH
                '''
            }
        }
        
        stage('Installation Python 3.13 si nécessaire') {
            when {
                // Exécuter seulement si Python 3.13 n'est pas trouvé
                expression {
                    sh(script: 'command -v python3.13', returnStatus: true) != 0
                }
            }
            steps {
                echo '🐍 Installation de Python 3.13...'
                script {
                    // Détection de la distribution
                    def osType = sh(script: '''
                        if [ -f /etc/os-release ]; then
                            . /etc/os-release
                            echo $ID
                        elif [ "$(uname)" = "Darwin" ]; then
                            echo "macos"
                        else
                            echo "unknown"
                        fi
                    ''', returnStdout: true).trim()
                    
                    echo "Système détecté: ${osType}"
                    
                    switch(osType) {
                        case 'ubuntu':
                        case 'debian':
                            sh '''
                                echo "Installation sur Ubuntu/Debian..."
                                sudo apt-get update
                                sudo apt-get install -y software-properties-common build-essential
                                
                                # Python 3.13 via deadsnakes PPA (Ubuntu)
                                if [ "$ID" = "ubuntu" ]; then
                                    sudo add-apt-repository -y ppa:deadsnakes/ppa
                                    sudo apt-get update
                                    sudo apt-get install -y python3.13 python3.13-venv python3.13-dev
                                # Ou compilation depuis source pour Debian
                                else
                                    echo "Compilation de Python 3.13 depuis source..."
                                    sudo apt-get install -y wget build-essential libssl-dev zlib1g-dev \
                                        libbz2-dev libreadline-dev libsqlite3-dev libncursesw5-dev \
                                        xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
                                    
                                    wget https://www.python.org/ftp/python/3.13.0/Python-3.13.0.tgz
                                    tar -xf Python-3.13.0.tgz
                                    cd Python-3.13.0
                                    ./configure --enable-optimizations
                                    make -j$(nproc)
                                    sudo make altinstall
                                    cd ..
                                    rm -rf Python-3.13.0 Python-3.13.0.tgz
                                fi
                                
                                # Vérification
                                python3.13 --version
                            '''
                            break
                            
                        case 'centos':
                        case 'rhel':
                        case 'fedora':
                            sh '''
                                echo "Installation sur CentOS/RHEL/Fedora..."
                                sudo dnf install -y gcc openssl-devel bzip2-devel libffi-devel zlib-devel
                                sudo dnf install -y wget make tk-devel xz-devel sqlite-devel
                                
                                wget https://www.python.org/ftp/python/3.13.0/Python-3.13.0.tgz
                                tar -xf Python-3.13.0.tgz
                                cd Python-3.13.0
                                ./configure --enable-optimizations
                                make -j$(nproc)
                                sudo make altinstall
                                cd ..
                                rm -rf Python-3.13.0 Python-3.13.0.tgz
                                
                                python3.13 --version
                            '''
                            break
                            
                        case 'macos':
                            sh '''
                                echo "Installation sur macOS..."
                                # Avec Homebrew
                                if command -v brew &> /dev/null; then
                                    brew update
                                    brew install python@3.13
                                    brew link --overwrite python@3.13
                                # Sinon installer depuis python.org
                                else
                                    echo "Installation via python.org..."
                                    curl -O https://www.python.org/ftp/python/3.13.0/python-3.13.0-macos11.pkg
                                    sudo installer -pkg python-3.13.0-macos11.pkg -target /
                                    rm python-3.13.0-macos11.pkg
                                fi
                                
                                # Vérifier l'installation
                                /usr/local/bin/python3.13 --version || python3.13 --version
                            '''
                            break
                            
                        default:
                            echo "⚠️ Système non supporté, tentative avec pyenv..."
                            sh '''
                                # Installation de pyenv
                                curl https://pyenv.run | bash
                                export PYENV_ROOT="$HOME/.pyenv"
                                [[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
                                eval "$(pyenv init -)"
                                
                                # Installation Python 3.13
                                pyenv install 3.13.0
                                pyenv global 3.13.0
                                
                                # Mise à jour du PATH
                                export PATH="$HOME/.pyenv/versions/3.13.0/bin:$PATH"
                                python --version
                            '''
                            break
                    }
                }
            }
        }
        
        stage('Setup Environment Python 3.13') {
            steps {
                echo '⚙️ Configuration de l\'environnement Python 3.13...'
                sh '''
                    echo "=== SÉLECTION DE PYTHON 3.13 ==="
                    
                    # Priorité d'exécution
                    PYTHON_CMD=""
                    if command -v python3.13 &> /dev/null; then
                        PYTHON_CMD="python3.13"
                    elif command -v python3 &> /dev/null && python3 --version 2>&1 | grep -q "3.13"; then
                        PYTHON_CMD="python3"
                    elif command -v python &> /dev/null && python --version 2>&1 | grep -q "3.13"; then
                        PYTHON_CMD="python"
                    elif [ -f "/usr/local/bin/python3.13" ]; then
                        PYTHON_CMD="/usr/local/bin/python3.13"
                    elif [ -f "/usr/bin/python3.13" ]; then
                        PYTHON_CMD="/usr/bin/python3.13"
                    else
                        echo "❌ ERREUR: Python 3.13 non trouvé"
                        echo "Liste finale des binaires Python:"
                        which -a python3 python || true
                        exit 1
                    fi
                    
                    echo "✅ Python sélectionné: $PYTHON_CMD"
                    $PYTHON_CMD --version
                    
                    # Création du virtualenv avec Python 3.13
                    echo "=== CRÉATION VIRTUALENV ==="
                    $PYTHON_CMD -m venv venv --clear --prompt "py3.13-django"
                    
                    # Activation
                    source venv/bin/activate
                    
                    echo "=== VÉRIFICATION VIRTUALENV ==="
                    which python
                    python --version
                    
                    echo "=== MISE À JOUR PIP ==="
                    python -m pip install --upgrade pip setuptools wheel
                    pip --version
                    
                    echo "=== CONFIGURATION PIP CACHE ==="
                    mkdir -p ${PIP_CACHE_DIR}
                    pip config set global.cache-dir ${PIP_CACHE_DIR}
                    
                    echo "✅ Environnement Python 3.13 configuré avec succès"
                '''
            }
        }
        
        stage('Installation Dépendances Django') {
            steps {
                echo '📦 Installation des dépendances Django...'
                sh '''
                    source venv/bin/activate
                    
                    echo "=== INSTALLATION DJANGO ==="
                    # Django compatible avec Python 3.13
                    pip install "Django>=5.0,<6.0"  # Django 6.0 n'existe pas encore, utiliser Django 5.x
                    
                    # Autres dépendances principales
                    pip install djangorestframework
                    pip install psycopg2-binary  # Si vous utilisez PostgreSQL
                    
                    echo "=== INSTALLATION OUTILS DÉVELOPPEMENT ==="
                    pip install flake8 pytest pytest-django pytest-cov
                    pip install bandit safety
                    pip install black isort  # Pour le formatage
                    
                    # Vérification des versions
                    echo "=== VÉRIFICATION VERSIONS ==="
                    python -c "import django; print(f'Django {django.__version__}')"
                    python -c "import sys; print(f'Python {sys.version}')"
                    
                    # Installation depuis requirements.txt si existant
                    if [ -f "requirements.txt" ]; then
                        echo "Installation depuis requirements.txt..."
                        # Nettoyer le fichier requirements.txt si nécessaire
                        grep -v "Django==" requirements.txt > requirements_clean.txt || cp requirements.txt requirements_clean.txt
                        pip install -r requirements_clean.txt
                        rm -f requirements_clean.txt
                    fi
                    
                    echo "✅ Dépendances installées avec succès"
                '''
            }
        }
        
        stage('Database Setup') {
            steps {
                echo '🗄️ Configuration de la base de données...'
                sh '''
                    source venv/bin/activate
                    export DJANGO_SETTINGS_MODULE=employe_project.settings
                    
                    echo "=== VÉRIFICATION MIGRATIONS ==="
                    # Test de connexion (pour SQLite, crée le fichier si besoin)
                    python -c "
                    import django
                    django.setup()
                    from django.db import connection
                    cursor = connection.cursor()
                    print('✓ Connexion BD OK')
                    "
                    
                    echo "=== APPLICATIONS DES MIGRATIONS ==="
                    python manage.py migrate --noinput
                    
                    echo "=== COLLECTE FICHIERS STATIQUES ==="
                    python manage.py collectstatic --noinput --clear || echo "Collecte statique ignorée"
                    
                    echo "✅ Base de données configurée"
                '''
            }
        }
        
        stage('Code Quality') {
            parallel {
                stage('Linting & Formatting') {
                    steps {
                        echo '🧹 Vérification du code...'
                        sh '''
                            source venv/bin/activate
                            
                            echo "=== BLACK (formatage) ==="
                            black --check --diff employe/ employe_project/ || true
                            
                            echo "=== ISORT (imports) ==="
                            isort --check-only --diff employe/ employe_project/ || true
                            
                            echo "=== FLAKE8 (linting) ==="
                            flake8 employe/ employe_project/ \
                                --max-line-length=100 \
                                --exclude=migrations,venv,env,.venv \
                                --format=junit-xml \
                                --output-file=flake8-report.xml || true
                        '''
                    }
                }
                
                stage('Security Scan') {
                    steps {
                        echo '🛡️ Analyse de sécurité...'
                        sh '''
                            source venv/bin/activate
                            
                            echo "=== SAFETY (dépendances) ==="
                            safety check --json --output safety-report.json || true
                            
                            echo "=== BANDIT (code) ==="
                            bandit -r employe/ employe_project/ \
                                -f json -o bandit-report.json \
                                --exclude="*/migrations/*,*/venv/*,*/env/*,*/.venv/*" || true
                            
                            # Rapport HTML pour bandit
                            bandit -r employe/ employe_project/ \
                                -f html -o bandit-report.html \
                                --exclude="*/migrations/*,*/venv/*,*/env/*,*/.venv/*" || true
                        '''
                    }
                }
            }
        }
        
        stage('Tests Django') {
            steps {
                echo '🧪 Exécution des tests...'
                sh '''
                    source venv/bin/activate
                    export DJANGO_SETTINGS_MODULE=employe_project.settings
                    
                    echo "=== TESTS DJANGO NATIFS ==="
                    # Tests Django avec sortie détaillée
                    python manage.py test --noinput --parallel=$(nproc 2>/dev/null || echo 2) --verbosity=2
                    
                    echo "=== TESTS AVEC PYTEST ==="
                    # Tests avec pytest pour meilleurs rapports
                    pytest employe/ employe_project/ \
                        --junitxml=pytest-report.xml \
                        --cov=employe \
                        --cov=employe_project \
                        --cov-report=xml \
                        --cov-report=html \
                        --cov-exclude="*/migrations/*,*/tests/*" \
                        --disable-warnings || true
                    
                    echo "=== RAPPORT COUVERTURE ==="
                    python -c "
                    import xml.etree.ElementTree as ET
                    try:
                        tree = ET.parse('coverage.xml')
                        root = tree.getroot()
                        line_rate = float(root.get('line-rate', 0)) * 100
                        branch_rate = float(root.get('branch-rate', 0)) * 100
                        print(f'Couverture lignes: {line_rate:.1f}%')
                        print(f'Couverture branches: {branch_rate:.1f}%')
                    except:
                        print('Rapport de couverture non disponible')
                    "
                '''
            }
        }
        
        stage('Django Health Check') {
            steps {
                echo '🏥 Vérifications Django approfondies...'
                sh '''
                    source venv/bin/activate
                    export DJANGO_SETTINGS_MODULE=employe_project.settings
                    
                    echo "=== VÉRIFICATIONS SYSTÈME ==="
                    python manage.py check --deploy --fail-level ERROR || true
                    
                    echo "=== ÉTAT DES MIGRATIONS ==="
                    python manage.py showmigrations --list
                    
                    echo "=== VÉRIFICATION ADMIN ==="
                    python manage.py shell -c "
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    try:
                        admin_count = User.objects.filter(is_superuser=True).count()
                        print(f'✓ Superutilisateurs: {admin_count}')
                    except:
                        print('⚠️ Impossible de vérifier les utilisateurs')
                    "
                    
                    echo "=== TEST SERVEUR DE DÉVELOPPEMENT ==="
                    # Test rapide du serveur
                    timeout 10 python manage.py runserver 0.0.0.0:8888 &
                    SERVER_PID=$!
                    sleep 3
                    if curl -f http://localhost:8888/ > /dev/null 2>&1; then
                        echo "✅ Serveur Django fonctionnel"
                    else
                        echo "⚠️ Serveur Django non accessible"
                    fi
                    kill $SERVER_PID 2>/dev/null || true
                '''
            }
        }
    }
    
    post {
        always {
            echo '🧹 Nettoyage et archivage...'
            
            // Archive des rapports de qualité
            archiveArtifacts(
                artifacts: '**/*-report.*, coverage.xml, .coverage',
                allowEmptyArchive: true
            )
            
            // Rapports JUnit
            junit(
                allowEmptyResults: true,
                testResults: '**/*-report.xml',
                healthScaleFactor: 100.0
            )
            
            // Rapport de couverture HTML
            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Couverture de Code',
                reportTitles: 'Couverture Python 3.13'
            ])
            
            // Rapport de sécurité
            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: false,
                reportDir: '.',
                reportFiles: 'bandit-report.html',
                reportName: 'Rapport Sécurité',
                reportTitles: 'Bandit Security Scan'
            ])
            
            // Nettoyage
            sh '''
                echo "=== NETTOYAGE ==="
                # Arrêt de tous les processus Python
                pkill -f "python.*runserver" 2>/dev/null || true
                pkill -f "python.*manage.py" 2>/dev/null || true
                
                # Suppression des fichiers temporaires
                rm -rf venv .venv __pycache__ */__pycache__ *.pyc
                rm -f db.sqlite3 test*.db .coverage
                rm -f *.log *.pid
                
                echo "✅ Nettoyage terminé"
            '''
        }
        
        success {
            echo '✅✅✅ Pipeline Django avec Python 3.13 réussi! ✅✅✅'
            script {
                // Notification optionnelle
                def pythonVersion = sh(script: 'source venv/bin/activate 2>/dev/null && python --version || echo "Unknown"', returnStdout: true).trim()
                def djangoVersion = sh(script: 'source venv/bin/activate 2>/dev/null && python -c "import django; print(django.__version__)" 2>/dev/null || echo "Unknown"', returnStdout: true).trim()
                
                echo """
                📊 RÉSUMÉ DU BUILD
                ==================
                Python: ${pythonVersion}
                Django: ${djangoVersion}
                Build: ${env.BUILD_NUMBER}
                Job: ${env.JOB_NAME}
                ==================
                """
                
                // Exemple Slack
                // slackSend(
                //     color: 'good',
                //     message: "✅ Build ${env.BUILD_NUMBER} réussi\nPython ${pythonVersion}\nDjango ${djangoVersion}"
                // )
            }
        }
        
        failure {
            echo '❌❌❌ Pipeline Django échouée! ❌❌❌'
            script {
                // Logs de débogage
                sh '''
                    echo "=== DERNIERS LOGS D'ERREUR ==="
                    tail -50 /var/log/syslog 2>/dev/null || dmesg | tail -20 2>/dev/null || echo "Pas de logs système"
                    
                    echo "=== ESPACE DISPONIBLE ==="
                    df -h .
                    
                    echo "=== MÉMOIRE ==="
                    free -h 2>/dev/null || echo "Commande free non disponible"
                    
                    echo "=== PROCESSUS PYTHON ==="
                    ps aux | grep -i python | head -20
                '''
                
                // slackSend(
                //     color: 'danger',
                //     message: "❌ Build ${env.BUILD_NUMBER} échoué\nVoir: ${env.BUILD_URL}"
                // )
            }
        }
        
        unstable {
            echo '⚠️ Pipeline instable (tests échoués)'
            // slackSend(
            //     color: 'warning',
            //     message: "⚠️ Build ${env.BUILD_NUMBER} instable\nTests échoués mais build OK"
            // )
        }
    }
}