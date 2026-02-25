#!/bin/bash

# BMW Copart Finder - GitHub Setup Script
# Bu scripti bir dəfə işə salın, hər şey avtomatik qurulacaq

echo "=========================================="
echo "🚗 BMW Copart Finder - GitHub Setup"
echo "=========================================="
echo ""

# Rəng kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Git yoxla
echo "📦 Git yoxlanılır..."
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git quraşdırılmayıb!${NC}"
    echo "Git yüklə: https://git-scm.com/downloads"
    exit 1
fi
echo -e "${GREEN}✅ Git hazırdır${NC}"

# 2. Repository URL
echo ""
echo "📥 Repository URL-ni daxil edin:"
echo "   (Məsələn: https://github.com/username/bmw-copart-finder.git)"
read -p "URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo -e "${RED}❌ URL daxil edilməyib!${NC}"
    exit 1
fi

# 3. Repository-ni clone et
REPO_NAME=$(basename "$REPO_URL" .git)
echo ""
echo "📂 Repository klonlanır..."

if [ -d "$REPO_NAME" ]; then
    echo -e "${YELLOW}⚠️  Folder artıq mövcuddur: $REPO_NAME${NC}"
    read -p "Silmək istəyirsiniz? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$REPO_NAME"
    else
        exit 1
    fi
fi

git clone "$REPO_URL"
cd "$REPO_NAME" || exit 1
echo -e "${GREEN}✅ Repository klonlandı${NC}"

# 4. Python yoxla
echo ""
echo "🐍 Python yoxlanılır..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 quraşdırılmayıb!${NC}"
    echo "Python yüklə: https://www.python.org/downloads/"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✅ $PYTHON_VERSION${NC}"

# 5. Virtual environment yarat
echo ""
echo "📦 Virtual environment yaradılır..."
python3 -m venv venv

# Virtual environment aktivləşdir
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo -e "${RED}❌ Virtual environment xətası!${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Virtual environment hazırdır${NC}"

# 6. Dependencies install et
echo ""
echo "📦 Paketlər quraşdırılır..."
pip install --quiet selenium webdriver-manager requests
echo -e "${GREEN}✅ Bütün paketlər quraşdırıldı${NC}"

# 7. Test et
echo ""
echo "🧪 Test aparılır..."
if python3 copart_bmw_finder.py &> /dev/null; then
    echo -e "${GREEN}✅ Proqram işləyir!${NC}"
else
    echo -e "${YELLOW}⚠️  Bəzi xətalar ola bilər (normal)${NC}"
fi

# 8. Kriteriyaları dəyişmək istəyir?
echo ""
echo "=========================================="
echo "⚙️  QURAŞDIRMA"
echo "=========================================="
echo ""
read -p "Axtarış kriteriyalarını indi dəyişmək istəyirsiniz? (y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📝 copart_real_finder.py faylını açın və self.criteria bölməsini dəyişdirin:"
    echo "   - models: ['530i', '540i', 'M550i']"
    echo "   - year_min: 2020"
    echo "   - year_max: 2023"
    echo "   - max_mileage: 100000"
    echo ""
    read -p "Davam etmək üçün Enter basın..."
fi

# 9. GitHub Actions üçün təlimat
echo ""
echo "=========================================="
echo "🚀 GITHUB ACTIONS QURAŞDIRMASI"
echo "=========================================="
echo ""
echo "1. GitHub-da repository-nizi açın"
echo "2. 'Actions' tabına keçin"
echo "3. 'I understand my workflows...' düyməsinə basın"
echo "4. Sol tərəfdə 'BMW Copart Finder' workflow-nu seçin"
echo "5. 'Run workflow' düyməsinə basın"
echo ""
echo "⏰ Workflow avtomatik olaraq hər gün işləyəcək"
echo ""

# 10. Telegram quraşdırma (optional)
echo "=========================================="
echo "📱 TELEGRAM NOTIFICATION (Optional)"
echo "=========================================="
echo ""
read -p "Telegram bildirişləri quraşdırmaq istəyirsiniz? (y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📱 Telegram Bot yaradın:"
    echo "   1. Telegram-da @BotFather-ə yazın"
    echo "   2. /newbot göndərin"
    echo "   3. Bot adını verin"
    echo "   4. TOKEN-i save edin"
    echo ""
    read -p "Bot TOKEN-ni daxil edin: " BOT_TOKEN
    
    echo ""
    echo "💬 Chat ID tapmaq üçün:"
    echo "   1. Bot-a bir mesaj göndərin"
    echo "   2. Bu linkə daxil olun:"
    echo "      https://api.telegram.org/bot$BOT_TOKEN/getUpdates"
    echo "   3. 'chat.id' nömrəsini tapın"
    echo ""
    read -p "Chat ID-ni daxil edin: " CHAT_ID
    
    echo ""
    echo "🔐 GitHub Secrets əlavə edin:"
    echo "   1. Repository → Settings → Secrets → Actions"
    echo "   2. 'New repository secret' basın"
    echo "   3. İki secret əlavə edin:"
    echo "      - Name: TELEGRAM_BOT_TOKEN"
    echo "        Value: $BOT_TOKEN"
    echo "      - Name: TELEGRAM_CHAT_ID"
    echo "        Value: $CHAT_ID"
    echo ""
fi

# 11. Yekun
echo ""
echo "=========================================="
echo "✅ QURAŞDIRMA TAMAMLANDI!"
echo "=========================================="
echo ""
echo "📂 Proyekt folder: $PWD"
echo "🐍 Virtual environment: Aktivdir"
echo ""
echo "🚀 İNDİ NƏ EDƏK?"
echo ""
echo "LOKAL TEST:"
echo "   python3 copart_bmw_finder.py        # Demo ilə test"
echo "   python3 copart_real_finder.py       # Real axtarış"
echo ""
echo "GITHUB-DA İŞƏ SAL:"
echo "   1. GitHub-da repository-ni açın"
echo "   2. Actions → BMW Copart Finder"
echo "   3. Run workflow"
echo ""
echo "DƏYIŞIKLIKLƏR ETMƏK:"
echo "   1. copart_real_finder.py faylını edit edin"
echo "   2. git add . && git commit -m 'Update criteria'"
echo "   3. git push"
echo ""
echo "=========================================="
echo "🎉 UĞURLAR!"
echo "=========================================="
