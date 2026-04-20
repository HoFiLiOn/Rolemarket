const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ========== КОНФИГУРАЦИЯ ==========
const TOKEN = '8786399001:AAF2GODnsIrCluHiFPH8XYC8uVMuPrDiSss';
const MASTER_IDS = [8388843828];

const DATA_DIR = path.join(__dirname, 'data');
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR);

const USERS_FILE = path.join(DATA_DIR, 'users.json');
const ROLES_FILE = path.join(DATA_DIR, 'roles.json');
const MARKET_FILE = path.join(DATA_DIR, 'market.json');
const REPORTS_FILE = path.join(DATA_DIR, 'reports.json');
const IDEAS_FILE = path.join(DATA_DIR, 'ideas.json');
const SETTINGS_FILE = path.join(DATA_DIR, 'settings.json');

const bot = new TelegramBot(TOKEN, { polling: true });

// ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========
function getMoscowTime() {
    const now = new Date();
    return new Date(now.getTime() + 3 * 60 * 60 * 1000);
}

function formatDate(date) {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}`;
}

function loadJSON(filePath, defaultValue = {}) {
    try {
        if (fs.existsSync(filePath)) {
            const data = fs.readFileSync(filePath, 'utf8');
            return JSON.parse(data);
        }
    } catch (e) {}
    return defaultValue;
}

function saveJSON(filePath, data) {
    try {
        fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
        return true;
    } catch (e) {
        console.error(e);
        return false;
    }
}

function isAdmin(userId) {
    if (MASTER_IDS.includes(userId)) return true;
    const admins = loadJSON(path.join(DATA_DIR, 'admins.json'));
    return admins.admin_list && admins.admin_list[userId];
}

function isMaster(userId) {
    return MASTER_IDS.includes(userId);
}

function getUser(userId) {
    const users = loadJSON(USERS_FILE);
    return users[userId];
}

function createUser(userId, username, firstName) {
    const users = loadJSON(USERS_FILE);
    if (!users[userId]) {
        users[userId] = {
            coins: 100,
            role: null,
            username: username,
            first_name: firstName,
            messages: 0,
            messages_today: 0,
            last_message_reset: null,
            daily_streak: 0,
            last_daily: null,
            invites: [],
            invited_by: null,
            referral_earned: 0,
            total_earned: 100,
            total_spent: 0,
            is_banned: false,
            ban_reason: null,
            registered_at: formatDate(getMoscowTime()),
            last_active: formatDate(getMoscowTime()),
            workshop_level: 1
        };
        saveJSON(USERS_FILE, users);
    }
    return users[userId];
}

function addCoins(userId, amount) {
    const users = loadJSON(USERS_FILE);
    if (users[userId]) {
        users[userId].coins += amount;
        users[userId].total_earned += amount;
        saveJSON(USERS_FILE, users);
        return true;
    }
    return false;
}

function removeCoins(userId, amount) {
    const users = loadJSON(USERS_FILE);
    if (users[userId]) {
        users[userId].coins = Math.max(0, users[userId].coins - amount);
        users[userId].total_spent += amount;
        saveJSON(USERS_FILE, users);
        return true;
    }
    return false;
}

function isBanned(userId) {
    const user = getUser(userId);
    return user ? user.is_banned : false;
}

// ========== РОЛИ ==========
function loadRoles() {
    const roles = loadJSON(ROLES_FILE);
    if (Object.keys(roles).length === 0) {
        const defaultRoles = {
            'Vip': { price: 12000, mult: 1.1 },
            'Pro': { price: 15000, mult: 1.2 },
            'Phoenix': { price: 25000, mult: 1.3 },
            'Dragon': { price: 40000, mult: 1.4 },
            'Elite': { price: 45000, mult: 1.5 },
            'Phantom': { price: 50000, mult: 1.6 },
            'Hydra': { price: 60000, mult: 1.7 },
            'Overlord': { price: 75000, mult: 1.8 },
            'Apex': { price: 90000, mult: 1.9 },
            'Quantum': { price: 100000, mult: 2.0 }
        };
        saveJSON(ROLES_FILE, defaultRoles);
        return defaultRoles;
    }
    return roles;
}

function saveRoles(roles) {
    saveJSON(ROLES_FILE, roles);
}

function getWorkshopBonus(level) {
    const settings = loadJSON(SETTINGS_FILE);
    const levels = settings.workshop_levels || {
        1: { price: 0, bonus: 0, max_lots: 1 },
        2: { price: 5000, bonus: 5, max_lots: 1 },
        3: { price: 10000, bonus: 10, max_lots: 2 },
        4: { price: 20000, bonus: 15, max_lots: 2 },
        5: { price: 35000, bonus: 20, max_lots: 3 },
        6: { price: 55000, bonus: 25, max_lots: 3 },
        7: { price: 80000, bonus: 30, max_lots: 4 },
        8: { price: 110000, bonus: 35, max_lots: 4 },
        9: { price: 150000, bonus: 40, max_lots: 5 },
        10: { price: 200000, bonus: 50, max_lots: 5 }
    };
    return levels[level] ? levels[level].bonus : 0;
}

function getWorkshopMaxLots(level) {
    const settings = loadJSON(SETTINGS_FILE);
    const levels = settings.workshop_levels || {
        1: { price: 0, bonus: 0, max_lots: 1 },
        2: { price: 5000, bonus: 5, max_lots: 1 },
        3: { price: 10000, bonus: 10, max_lots: 2 },
        4: { price: 20000, bonus: 15, max_lots: 2 },
        5: { price: 35000, bonus: 20, max_lots: 3 },
        6: { price: 55000, bonus: 25, max_lots: 3 },
        7: { price: 80000, bonus: 30, max_lots: 4 },
        8: { price: 110000, bonus: 35, max_lots: 4 },
        9: { price: 150000, bonus: 40, max_lots: 5 },
        10: { price: 200000, bonus: 50, max_lots: 5 }
    };
    return levels[level] ? levels[level].max_lots : 1;
}

function getWorkshopNextPrice(level) {
    const settings = loadJSON(SETTINGS_FILE);
    const levels = settings.workshop_levels || {
        1: { price: 0, bonus: 0, max_lots: 1 },
        2: { price: 5000, bonus: 5, max_lots: 1 },
        3: { price: 10000, bonus: 10, max_lots: 2 },
        4: { price: 20000, bonus: 15, max_lots: 2 },
        5: { price: 35000, bonus: 20, max_lots: 3 },
        6: { price: 55000, bonus: 25, max_lots: 3 },
        7: { price: 80000, bonus: 30, max_lots: 4 },
        8: { price: 110000, bonus: 35, max_lots: 4 },
        9: { price: 150000, bonus: 40, max_lots: 5 },
        10: { price: 200000, bonus: 50, max_lots: 5 }
    };
    const nextLevel = level + 1;
    return levels[nextLevel] ? levels[nextLevel].price : null;
}

function upgradeWorkshop(userId) {
    const user = getUser(userId);
    if (!user) return { success: false, msg: "Ошибка" };
    const currentLevel = user.workshop_level || 1;
    const nextPrice = getWorkshopNextPrice(currentLevel);
    if (!nextPrice) return { success: false, msg: "Максимальный уровень достигнут" };
    if (user.coins < nextPrice) return { success: false, msg: `Не хватает монет. Нужно ${nextPrice}💰` };
    removeCoins(userId, nextPrice);
    const users = loadJSON(USERS_FILE);
    users[userId].workshop_level = currentLevel + 1;
    saveJSON(USERS_FILE, users);
    return { success: true, msg: `Мастерская улучшена до ${currentLevel + 1} уровня! +${getWorkshopBonus(currentLevel + 1)}% к доходу` };
}

function getMultiplier(userId) {
    const user = getUser(userId);
    if (!user) return 1.0;
    const roles = loadRoles();
    const roleMult = (user.role && roles[user.role]) ? roles[user.role].mult : 1.0;
    const workshopBonus = getWorkshopBonus(user.workshop_level || 1);
    return roleMult * (1 + workshopBonus / 100);
}

function addMessage(userId) {
    if (isBanned(userId)) return false;
    const user = getUser(userId);
    if (!user) return false;
    const now = getMoscowTime();
    const today = formatDate(now).slice(0, 10);
    if (user.last_message_reset !== today) {
        user.messages_today = 0;
        user.last_message_reset = today;
    }
    if (user.messages_today >= 500) return false;
    const base = Math.floor(Math.random() * 5) + 1;
    const mult = getMultiplier(userId);
    const earn = Math.floor(base * mult);
    const users = loadJSON(USERS_FILE);
    users[userId].messages += 1;
    users[userId].messages_today += 1;
    users[userId].coins += earn;
    users[userId].total_earned += earn;
    users[userId].last_active = formatDate(now);
    if (users[userId].messages % 100 === 0) {
        const bonus = 500;
        users[userId].coins += bonus;
        users[userId].total_earned += bonus;
        try {
            bot.sendMessage(userId, `🎉 <b>Бонус!</b>\n\n📊 ${users[userId].messages} сообщений\n💰 +${bonus} монет`, { parse_mode: 'HTML' });
        } catch(e) {}
    }
    saveJSON(USERS_FILE, users);
    return true;
}

function getDaily(userId) {
    const user = getUser(userId);
    if (!user) return { bonus: 0, msg: "Ошибка" };
    const today = formatDate(getMoscowTime()).slice(0, 10);
    if (user.last_daily === today) return { bonus: 0, msg: "❌ Бонус уже получен сегодня!" };
    let streak = (user.daily_streak || 0) + 1;
    let bonus, extra = "";
    if (streak >= 15) {
        bonus = Math.floor(Math.random() * 401) + 400;
        extra = "✨ Супер бонус! ✨";
    } else if (streak >= 8) {
        bonus = Math.floor(Math.random() * 201) + 200;
        extra = "⭐️ Отлично! ⭐️";
    } else if (streak >= 4) {
        bonus = Math.floor(Math.random() * 101) + 100;
        extra = "👍 Хорошо! 👍";
    } else {
        bonus = Math.floor(Math.random() * 51) + 50;
        extra = "";
    }
    const mult = getMultiplier(userId);
    bonus = Math.floor(bonus * mult);
    const users = loadJSON(USERS_FILE);
    users[userId].last_daily = today;
    users[userId].daily_streak = streak;
    users[userId].coins += bonus;
    users[userId].total_earned += bonus;
    saveJSON(USERS_FILE, users);
    let msg = `🎁 +${bonus}💰\n🔥 Серия: ${streak} дн.`;
    if (extra) msg += `\n${extra}`;
    return { bonus, msg };
}

function buyRole(userId, roleName) {
    const user = getUser(userId);
    if (!user) return { success: false, msg: "Ошибка" };
    const roles = loadRoles();
    if (!roles[roleName]) return { success: false, msg: "Роль не найдена" };
    const price = roles[roleName].price;
    if (user.coins < price) return { success: false, msg: `Нужно ${price}💰\n💰 У тебя: ${user.coins}💰` };
    const oldRole = user.role;
    let cashback = 0;
    if (oldRole && roles[oldRole] && roles[oldRole].price > 0) {
        cashback = Math.floor(roles[oldRole].price * 0.1);
    }
    removeCoins(userId, price);
    if (cashback > 0) addCoins(userId, cashback);
    const users = loadJSON(USERS_FILE);
    users[userId].role = roleName;
    saveJSON(USERS_FILE, users);
    const inviter = user.invited_by;
    if (inviter) {
        const bonus = Math.floor(price * 0.1);
        addCoins(inviter, bonus);
        try {
            bot.sendMessage(inviter, `🎉 <b>Бонус!</b>\n\n👤 ${user.first_name} купил ${roleName}\n💰 +${bonus} монет`, { parse_mode: 'HTML' });
        } catch(e) {}
    }
    let msg = `✅ <b>Поздравляю!</b>\n\n🎭 Роль: ${roleName}\n💰 Цена: ${price}💰\n📈 Множитель: x${roles[roleName].mult}`;
    if (cashback > 0) msg += `\n💸 Кешбэк: ${cashback}💰`;
    return { success: true, msg };
}

function addInvite(inviter, invited) {
    const users = loadJSON(USERS_FILE);
    if (!users[inviter].invites) users[inviter].invites = [];
    if (!users[inviter].invites.includes(invited)) {
        users[inviter].invites.push(invited);
        users[inviter].coins += 100;
        users[inviter].referral_earned = (users[inviter].referral_earned || 0) + 100;
        saveJSON(USERS_FILE, users);
        try {
            bot.sendMessage(inviter, `🎉 <b>Новый реферал!</b>\n\n👤 ${users[invited].first_name}\n💰 +100 монет`, { parse_mode: 'HTML' });
        } catch(e) {}
        return true;
    }
    return false;
}

function checkReferralReward(invitedId) {
    const invited = getUser(invitedId);
    if (!invited) return;
    const inviter = invited.invited_by;
    if (!inviter) return;
    if (invited.messages >= 50) {
        const users = loadJSON(USERS_FILE);
        const key = `rewarded_${invitedId}`;
        if (!users[inviter][key]) {
            users[inviter].coins += 200;
            users[inviter].referral_earned = (users[inviter].referral_earned || 0) + 200;
            users[inviter][key] = true;
            saveJSON(USERS_FILE, users);
            try {
                bot.sendMessage(inviter, `🎉 <b>Бонус за активность!</b>\n\n👤 ${invited.first_name} написал 50 сообщений\n💰 +200 монет`, { parse_mode: 'HTML' });
            } catch(e) {}
        }
    }
}

// ========== РЫНОК ==========
function loadMarket() {
    const market = loadJSON(MARKET_FILE);
    if (Object.keys(market).length === 0) {
        return { lots: [], next_id: 1 };
    }
    return market;
}

function saveMarket(market) {
    saveJSON(MARKET_FILE, market);
}

function getMarketCommission(price) {
    const settings = loadJSON(SETTINGS_FILE);
    const tiers = settings.market_commission_tiers || [
        { max_price: 10000, commission: 30 },
        { max_price: 30000, commission: 15 },
        { max_price: 999999, commission: 10 }
    ];
    for (const tier of tiers) {
        if (price <= tier.max_price) return tier.commission;
    }
    return 10;
}

function getMarketMinPrice(roleName) {
    const settings = loadJSON(SETTINGS_FILE);
    const minPrices = settings.market_min_prices || {
        'Vip': 8000, 'Pro': 10000, 'Phoenix': 15000, 'Dragon': 25000,
        'Elite': 30000, 'Phantom': 35000, 'Hydra': 45000, 'Overlord': 55000,
        'Apex': 70000, 'Quantum': 80000
    };
    return minPrices[roleName] || 1000;
}

function addMarketLot(userId, roleName, price) {
    const user = getUser(userId);
    if (!user) return { success: false, msg: "Ошибка" };
    if (user.role !== roleName) return { success: false, msg: "Вы можете продавать только свою текущую роль" };
    const workshopLevel = user.workshop_level || 1;
    const maxLots = getWorkshopMaxLots(workshopLevel);
    const market = loadMarket();
    const userLots = market.lots.filter(lot => lot.seller_id === userId);
    if (userLots.length >= maxLots) return { success: false, msg: `Вы можете выставить только ${maxLots} лот(ов). Улучшите Мастерскую` };
    const minPrice = getMarketMinPrice(roleName);
    if (price < minPrice) return { success: false, msg: `Минимальная цена для этой роли: ${minPrice}💰` };
    const settings = loadJSON(SETTINGS_FILE);
    const lotDays = settings.market_lot_days || 7;
    const lot = {
        id: market.next_id,
        seller_id: userId,
        seller_name: user.first_name,
        seller_username: user.username,
        role_name: roleName,
        price: price,
        created_at: getMoscowTime().toISOString(),
        expires_at: new Date(getMoscowTime().getTime() + lotDays * 24 * 60 * 60 * 1000).toISOString()
    };
    market.lots.push(lot);
    market.next_id++;
    saveMarket(market);
    const users = loadJSON(USERS_FILE);
    users[userId].role = null;
    saveJSON(USERS_FILE, users);
    return { success: true, msg: `Роль ${roleName} выставлена на продажу за ${price}💰` };
}

function removeMarketLot(lotId, userId) {
    const market = loadMarket();
    const lotIndex = market.lots.findIndex(l => l.id === lotId && l.seller_id === userId);
    if (lotIndex === -1) return { success: false, msg: "Лот не найден" };
    const lot = market.lots[lotIndex];
    const users = loadJSON(USERS_FILE);
    users[userId].role = lot.role_name;
    saveJSON(USERS_FILE, users);
    market.lots.splice(lotIndex, 1);
    saveMarket(market);
    return { success: true, msg: `Лот #${lotId} снят, роль ${lot.role_name} возвращена` };
}

function buyMarketLot(lotId, buyerId) {
    const market = loadMarket();
    const lotIndex = market.lots.findIndex(l => l.id === lotId);
    if (lotIndex === -1) return { success: false, msg: "Лот не найден" };
    const lot = market.lots[lotIndex];
    if (lot.seller_id === buyerId) return { success: false, msg: "Нельзя купить свой лот" };
    const buyer = getUser(buyerId);
    if (!buyer) return { success: false, msg: "Ошибка" };
    const price = lot.price;
    if (buyer.coins < price) return { success: false, msg: `Не хватает монет. Нужно ${price}💰` };
    if (new Date(lot.expires_at) < getMoscowTime()) {
        const users = loadJSON(USERS_FILE);
        users[lot.seller_id].role = lot.role_name;
        saveJSON(USERS_FILE, users);
        market.lots.splice(lotIndex, 1);
        saveMarket(market);
        return { success: false, msg: "Лот истёк" };
    }
    const commissionPercent = getMarketCommission(price);
    const commission = Math.floor(price * commissionPercent / 100);
    const sellerGets = price - commission;
    removeCoins(buyerId, price);
    addCoins(lot.seller_id, sellerGets);
    const users = loadJSON(USERS_FILE);
    users[buyerId].role = lot.role_name;
    saveJSON(USERS_FILE, users);
    market.lots.splice(lotIndex, 1);
    saveMarket(market);
    try {
        bot.sendMessage(lot.seller_id, `💰 <b>Ваш лот продан!</b>\n\n🎭 Роль: ${lot.role_name}\n💰 Цена: ${price}💰\n💸 Комиссия: ${commission}💰\n💵 Вы получили: ${sellerGets}💰`, { parse_mode: 'HTML' });
    } catch(e) {}
    return { success: true, msg: `✅ Вы купили роль ${lot.role_name} за ${price}💰` };
}

function getUserLots(userId) {
    const market = loadMarket();
    return market.lots.filter(lot => lot.seller_id === userId);
}

function getAllLots() {
    const market = loadMarket();
    return market.lots;
}

function cleanupExpiredLots() {
    const market = loadMarket();
    const now = getMoscowTime();
    let removed = 0;
    for (let i = market.lots.length - 1; i >= 0; i--) {
        const lot = market.lots[i];
        if (new Date(lot.expires_at) < now) {
            const users = loadJSON(USERS_FILE);
            users[lot.seller_id].role = lot.role_name;
            saveJSON(USERS_FILE, users);
            market.lots.splice(i, 1);
            removed++;
        }
    }
    if (removed) saveMarket(market);
    return removed;
}

// ========== ОТЧЁТЫ И ИДЕИ ==========
function saveReport(userId, username, firstName, text, fileId = null) {
    const reports = loadJSON(REPORTS_FILE);
    if (!reports.list) reports.list = [];
    const reportId = reports.list.length + 1;
    reports.list.push({
        id: reportId,
        user_id: userId,
        username: username,
        first_name: firstName,
        text: text,
        status: 'new',
        created_at: getMoscowTime().toISOString()
    });
    saveJSON(REPORTS_FILE, reports);
    const mention = username ? `@${username}` : firstName;
    try {
        bot.sendMessage(MASTER_IDS[0], `📝 <b>Новый отчёт</b>\n\nОт: ${mention} (ID: ${userId})\n\n${text}`, { parse_mode: 'HTML' });
    } catch(e) {}
    return reportId;
}

function saveIdea(userId, username, firstName, text) {
    const ideas = loadJSON(IDEAS_FILE);
    if (!ideas.list) ideas.list = [];
    const ideaId = ideas.list.length + 1;
    ideas.list.push({
        id: ideaId,
        user_id: userId,
        username: username,
        first_name: firstName,
        text: text,
        status: 'new',
        created_at: getMoscowTime().toISOString()
    });
    saveJSON(IDEAS_FILE, ideas);
    const mention = username ? `@${username}` : firstName;
    try {
        bot.sendMessage(MASTER_IDS[0], `💡 <b>Новая идея</b>\n\nОт: ${mention} (ID: ${userId})\n\n${text}`, { parse_mode: 'HTML' });
    } catch(e) {}
    return ideaId;
}

function getReportsList() {
    const reports = loadJSON(REPORTS_FILE);
    return reports.list || [];
}

function getIdeasList() {
    const ideas = loadJSON(IDEAS_FILE);
    return ideas.list || [];
}

function updateReportStatus(reportId, status) {
    const reports = loadJSON(REPORTS_FILE);
    const report = reports.list.find(r => r.id === reportId);
    if (report) {
        report.status = status;
        saveJSON(REPORTS_FILE, reports);
        return true;
    }
    return false;
}

function updateIdeaStatus(ideaId, status) {
    const ideas = loadJSON(IDEAS_FILE);
    const idea = ideas.list.find(i => i.id === ideaId);
    if (idea) {
        idea.status = status;
        saveJSON(IDEAS_FILE, ideas);
        return true;
    }
    return false;
}

function deleteReport(reportId) {
    const reports = loadJSON(REPORTS_FILE);
    reports.list = reports.list.filter(r => r.id !== reportId);
    saveJSON(REPORTS_FILE, reports);
    return true;
}

function deleteIdea(ideaId) {
    const ideas = loadJSON(IDEAS_FILE);
    ideas.list = ideas.list.filter(i => i.id !== ideaId);
    saveJSON(IDEAS_FILE, ideas);
    return true;
}

function getStats() {
    const users = loadJSON(USERS_FILE);
    const total = Object.keys(users).length;
    let coins = 0, msgs = 0, banned = 0, withRole = 0, active = 0;
    const today = formatDate(getMoscowTime()).slice(0, 10);
    for (const uid in users) {
        const u = users[uid];
        coins += u.coins || 0;
        msgs += u.messages || 0;
        if (u.is_banned) banned++;
        if (u.role) withRole++;
        if (u.last_active && u.last_active.slice(0, 10) === today) active++;
    }
    return { total, coins, msgs, banned, withRole, active };
}

// ========== КЛАВИАТУРЫ ==========
function getMainMenu(userId) {
    const markup = {
        inline_keyboard: [
            [
                { text: "🛍️ Магазин", callback_data: "shop" },
                { text: "👤 Профиль", callback_data: "profile" }
            ],
            [
                { text: "🔧 Мастерская", callback_data: "workshop" },
                { text: "💰 Рынок", callback_data: "market" }
            ],
            [
                { text: "🎁 Бонус", callback_data: "bonus" },
                { text: "📊 Топ", callback_data: "top" }
            ],
            [
                { text: "❓ Помощь", callback_data: "help" },
                { text: "📝 Обратная связь", callback_data: "feedback" }
            ]
        ]
    };
    if (isAdmin(userId)) {
        markup.inline_keyboard.push([{ text: "🔧 Админ панель", callback_data: "admin_panel" }]);
    }
    return markup;
}

function getBackButton() {
    return { inline_keyboard: [[{ text: "◀️ Назад", callback_data: "back" }]] };
}

function getShopMenu(page = 1) {
    const roles = loadRoles();
    const items = Object.entries(roles);
    const perPage = 3;
    const total = Math.ceil(items.length / perPage);
    if (page < 1) page = 1;
    if (page > total) page = total;
    const start = (page - 1) * perPage;
    const end = start + perPage;
    const markup = { inline_keyboard: [] };
    for (let i = start; i < end && i < items.length; i++) {
        const [name, data] = items[i];
        markup.inline_keyboard.push([{ text: `${name} — ${data.price}💰 (x${data.mult})`, callback_data: `buy_${name}` }]);
    }
    const nav = [];
    if (page > 1) nav.push({ text: "◀️", callback_data: `shop_page_${page-1}` });
    if (page < total) nav.push({ text: "▶️", callback_data: `shop_page_${page+1}` });
    if (nav.length) markup.inline_keyboard.push(nav);
    markup.inline_keyboard.push([{ text: "◀️ Назад", callback_data: "back" }]);
    return { markup, page, total };
}

function getMarketMenu(page = 1) {
    const lots = getAllLots();
    const perPage = 3;
    const total = Math.ceil(lots.length / perPage) || 1;
    if (page < 1) page = 1;
    if (page > total) page = total;
    const start = (page - 1) * perPage;
    const end = start + perPage;
    const markup = { inline_keyboard: [] };
    for (let i = start; i < end && i < lots.length; i++) {
        const lot = lots[i];
        const seller = lot.seller_username ? `@${lot.seller_username}` : lot.seller_name;
        markup.inline_keyboard.push([{ text: `#${lot.id} ${lot.role_name} — ${lot.price}💰 (${seller})`, callback_data: `lot_${lot.id}` }]);
    }
    const nav = [];
    if (page > 1) nav.push({ text: "◀️", callback_data: `market_page_${page-1}` });
    if (page < total) nav.push({ text: "▶️", callback_data: `market_page_${page+1}` });
    if (nav.length) markup.inline_keyboard.push(nav);
    markup.inline_keyboard.push([{ text: "💰 Выставить роль", callback_data: "market_sell" }]);
    markup.inline_keyboard.push([{ text: "📦 Мои лоты", callback_data: "market_my_lots" }]);
    markup.inline_keyboard.push([{ text: "◀️ Назад", callback_data: "back" }]);
    return { markup, page, total };
}

function getWorkshopMenu(userId) {
    const user = getUser(userId);
    const level = user.workshop_level || 1;
    const bonus = getWorkshopBonus(level);
    const maxLots = getWorkshopMaxLots(level);
    const nextPrice = getWorkshopNextPrice(level);
    const markup = { inline_keyboard: [] };
    if (nextPrice) {
        markup.inline_keyboard.push([{ text: `⚡️ Улучшить — ${nextPrice}💰`, callback_data: "workshop_upgrade" }]);
    }
    markup.inline_keyboard.push([{ text: "◀️ Назад", callback_data: "back" }]);
    return { markup, level, bonus, maxLots, nextPrice };
}

function getAdminPanel() {
    return {
        inline_keyboard: [
            [{ text: "📊 Статистика", callback_data: "admin_stats" }, { text: "👥 Пользователи", callback_data: "admin_users" }],
            [{ text: "💰 Выдать монеты", callback_data: "admin_add_coins" }, { text: "💸 Забрать монеты", callback_data: "admin_remove_coins" }],
            [{ text: "🎭 Выдать роль", callback_data: "admin_give_role" }, { text: "➕ Создать роль", callback_data: "admin_add_role" }],
            [{ text: "✏️ Редакт. роль", callback_data: "admin_edit_role" }, { text: "🗑 Удалить роль", callback_data: "admin_del_role" }],
            [{ text: "📋 Список ролей", callback_data: "admin_list_roles" }, { text: "🛒 Управление рынком", callback_data: "admin_market" }],
            [{ text: "🔧 Настройки мастерской", callback_data: "admin_workshop" }, { text: "📝 Отчёты", callback_data: "admin_reports" }],
            [{ text: "💡 Идеи", callback_data: "admin_ideas" }, { text: "🚫 Забанить", callback_data: "admin_ban" }],
            [{ text: "✅ Разбанить", callback_data: "admin_unban" }, { text: "👑 Добавить админа", callback_data: "admin_add_admin" }],
            [{ text: "🗑 Удалить админа", callback_data: "admin_remove_admin" }, { text: "📢 Рассылка", callback_data: "admin_mail" }],
            [{ text: "🎁 Промокоды", callback_data: "admin_promo" }, { text: "📦 Бэкап", callback_data: "admin_backup" }],
            [{ text: "◀️ Назад", callback_data: "back" }]
        ]
    };
}

function getUsersListMenu(page = 1) {
    const users = loadJSON(USERS_FILE);
    const items = Object.entries(users);
    const perPage = 10;
    const total = Math.ceil(items.length / perPage) || 1;
    if (page < 1) page = 1;
    if (page > total) page = total;
    const start = (page - 1) * perPage;
    const end = start + perPage;
    const markup = { inline_keyboard: [] };
    for (let i = start; i < end && i < items.length; i++) {
        const [uid, data] = items[i];
        const name = data.first_name || 'User';
        markup.inline_keyboard.push([{ text: `${name} — ${data.coins}💰`, callback_data: `user_${uid}` }]);
    }
    const nav = [];
    if (page > 1) nav.push({ text: "◀️", callback_data: `users_page_${page-1}` });
    if (page < total) nav.push({ text: "▶️", callback_data: `users_page_${page+1}` });
    if (nav.length) markup.inline_keyboard.push(nav);
    markup.inline_keyboard.push([{ text: "◀️ Назад", callback_data: "admin_panel" }]);
    return { markup, page, total };
}

function getUserActionsMenu(targetId) {
    return {
        inline_keyboard: [
            [{ text: "💰 Выдать монеты", callback_data: `user_add_coins_${targetId}` }, { text: "💸 Забрать монеты", callback_data: `user_remove_coins_${targetId}` }],
            [{ text: "🎭 Выдать роль", callback_data: `user_give_role_${targetId}` }, { text: "🚫 Забанить", callback_data: `user_ban_${targetId}` }],
            [{ text: "✅ Разбанить", callback_data: `user_unban_${targetId}` }, { text: "◀️ Назад", callback_data: "admin_users" }]
        ]
    };
}

function getReportsListMenu(page = 1) {
    const reports = getReportsList().reverse();
    const perPage = 5;
    const total = Math.ceil(reports.length / perPage) || 1;
    if (page < 1) page = 1;
    if (page > total) page = total;
    const start = (page - 1) * perPage;
    const end = start + perPage;
    const markup = { inline_keyboard: [] };
    for (let i = start; i < end && i < reports.length; i++) {
        const r = reports[i];
        const status = r.status === 'new' ? '🔴' : '🟢';
        const name = r.first_name || `User_${r.user_id}`;
        markup.inline_keyboard.push([{ text: `${status} #${r.id} — ${name}`, callback_data: `report_${r.id}` }]);
    }
    const nav = [];
    if (page > 1) nav.push({ text: "◀️", callback_data: `reports_page_${page-1}` });
    if (page < total) nav.push({ text: "▶️", callback_data: `reports_page_${page+1}` });
    if (nav.length) markup.inline_keyboard.push(nav);
    markup.inline_keyboard.push([{ text: "◀️ Назад", callback_data: "admin_panel" }]);
    return { markup, page, total };
}

function getIdeasListMenu(page = 1) {
    const ideas = getIdeasList().reverse();
    const perPage = 5;
    const total = Math.ceil(ideas.length / perPage) || 1;
    if (page < 1) page = 1;
    if (page > total) page = total;
    const start = (page - 1) * perPage;
    const end = start + perPage;
    const markup = { inline_keyboard: [] };
    for (let i = start; i < end && i < ideas.length; i++) {
        const idea = ideas[i];
        const status = idea.status === 'new' ? '🔴' : '🟢';
        const name = idea.first_name || `User_${idea.user_id}`;
        markup.inline_keyboard.push([{ text: `${status} #${idea.id} — ${name}`, callback_data: `idea_${idea.id}` }]);
    }
    const nav = [];
    if (page > 1) nav.push({ text: "◀️", callback_data: `ideas_page_${page-1}` });
    if (page < total) nav.push({ text: "▶️", callback_data: `ideas_page_${page+1}` });
    if (nav.length) markup.inline_keyboard.push(nav);
    markup.inline_keyboard.push([{ text: "◀️ Назад", callback_data: "admin_panel" }]);
    return { markup, page, total };
}

function getMarketAdminMenu(page = 1) {
    const lots = getAllLots();
    const perPage = 5;
    const total = Math.ceil(lots.length / perPage) || 1;
    if (page < 1) page = 1;
    if (page > total) page = total;
    const start = (page - 1) * perPage;
    const end = start + perPage;
    const markup = { inline_keyboard: [] };
    for (let i = start; i < end && i < lots.length; i++) {
        const lot = lots[i];
        const seller = lot.seller_username ? `@${lot.seller_username}` : lot.seller_name;
        markup.inline_keyboard.push([{ text: `#${lot.id} ${lot.role_name} — ${lot.price}💰 (${seller})`, callback_data: `admin_lot_${lot.id}` }]);
    }
    const nav = [];
    if (page > 1) nav.push({ text: "◀️", callback_data: `admin_lots_page_${page-1}` });
    if (page < total) nav.push({ text: "▶️", callback_data: `admin_lots_page_${page+1}` });
    if (nav.length) markup.inline_keyboard.push(nav);
    markup.inline_keyboard.push([{ text: "◀️ Назад", callback_data: "admin_panel" }]);
    return { markup, page, total };
}

function getFeedbackMenu() {
    return {
        inline_keyboard: [
            [{ text: "🐞 Сообщить о баге", callback_data: "send_report" }],
            [{ text: "💡 Предложить идею", callback_data: "send_idea" }],
            [{ text: "◀️ Назад", callback_data: "back" }]
        ]
    };
}

// ========== КОМАНДЫ ==========
bot.onText(/\/startrole|\/menu/, (msg) => {
    const chatId = msg.chat.id;
    if (msg.chat.type !== 'private') {
        bot.sendMessage(chatId, "Используй команду в личных сообщениях");
        return;
    }
    const userId = msg.from.id;
    if (isBanned(userId)) {
        bot.sendMessage(userId, "🚫 <b>Вы забанены</b>", { parse_mode: 'HTML' });
        return;
    }
    const user = createUser(userId, msg.from.username, msg.from.first_name);
    if (msg.text.startsWith('/startrole')) {
        const args = msg.text.split(' ');
        if (args.length > 1) {
            try {
                const inviter = parseInt(args[1]);
                if (inviter !== userId && !isMaster(inviter)) {
                    if (getUser(inviter)) {
                        addInvite(inviter, userId);
                        const users = loadJSON(USERS_FILE);
                        users[userId].invited_by = inviter;
                        saveJSON(USERS_FILE, users);
                    }
                }
            } catch(e) {}
        }
    }
    const role = user.role || "Нет роли";
    const mult = getMultiplier(userId);
    const workshopLevel = user.workshop_level || 1;
    const workshopBonus = getWorkshopBonus(workshopLevel);
    const text = `🌟 <b>Role Shop Bot</b>

Привет! Твой магазин ролей.

💰 <b>Что можно делать:</b>
• Писать в чат → получать монеты
• Покупать роли → увеличивать доход
• Улучшать мастерскую → повышать бонус
• Продавать роли на рынке
• Забирать ежедневный бонус
• Приглашать друзей

┌ 👤 <b>${user.first_name}</b>
├ 🎭 Роль: ${role}
├ 📈 Множитель: x${mult.toFixed(1)}
├ 🔧 Мастерская: ${workshopLevel} ур. (+${workshopBonus}%)
├ 💰 Баланс: ${user.coins}💰
├ 📊 Сообщений: ${user.messages}
└ 🔥 Серия: ${user.daily_streak || 0} дн.

👇 <b>Выбери действие:</b>`;
    bot.sendMessage(userId, text, { parse_mode: 'HTML', reply_markup: getMainMenu(userId) });
});

bot.onText(/\/daily/, (msg) => {
    const chatId = msg.chat.id;
    if (msg.chat.type !== 'private') return;
    const userId = msg.from.id;
    if (isBanned(userId)) {
        bot.sendMessage(userId, "🚫 Вы забанены", { parse_mode: 'HTML' });
        return;
    }
    const { bonus, msg: resultMsg } = getDaily(userId);
    bot.sendMessage(userId, resultMsg, { parse_mode: 'HTML' });
});

bot.onText(/\/admin/, (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;
    if (!isAdmin(userId)) {
        bot.sendMessage(chatId, "Нет доступа");
        return;
    }
    const user = getUser(userId);
    const text = `🔧 <b>Админ панель</b>\n\n👑 <b>${user.first_name}</b>\n📊 Статус: ${isMaster(userId) ? 'Владелец' : 'Администратор'}\n\n👇 <b>Выбери действие:</b>`;
    bot.sendMessage(userId, text, { parse_mode: 'HTML', reply_markup: getAdminPanel() });
});

// ========== ОБРАБОТЧИК КНОПОК ==========
bot.on('callback_query', (query) => {
    const userId = query.from.id;
    const data = query.data;
    const chatId = query.message.chat.id;
    const messageId = query.message.message_id;
    
    if (isBanned(userId)) {
        bot.answerCallbackQuery(query.id, { text: "Вы забанены", show_alert: true });
        return;
    }
    const user = createUser(userId, query.from.username, query.from.first_name);
    
    // Назад
    if (data === "back") {
        const role = user.role || "Нет роли";
        const mult = getMultiplier(userId);
        const workshopLevel = user.workshop_level || 1;
        const workshopBonus = getWorkshopBonus(workshopLevel);
        const text = `🌟 <b>Role Shop Bot</b>

┌ 👤 <b>${user.first_name}</b>
├ 🎭 Роль: ${role}
├ 📈 Множитель: x${mult.toFixed(1)}
├ 🔧 Мастерская: ${workshopLevel} ур. (+${workshopBonus}%)
├ 💰 Баланс: ${user.coins}💰
├ 📊 Сообщений: ${user.messages}
└ 🔥 Серия: ${user.daily_streak || 0} дн.

👇 <b>Выбери действие:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: getMainMenu(userId) });
        bot.answerCallbackQuery(query.id);
        return;
    }
    
    // Магазин
    if (data === "shop") {
        const { markup, page, total } = getShopMenu(1);
        const text = `🛍️ <b>Магазин ролей</b>\n\n💰 Баланс: ${user.coins}💰\n📄 Страница ${page}/${total}\n\n👇 <b>Выбери роль:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("shop_page_")) {
        const page = parseInt(data.split('_')[2]);
        const { markup, page: newPage, total } = getShopMenu(page);
        const text = `🛍️ <b>Магазин ролей</b>\n\n💰 Баланс: ${user.coins}💰\n📄 Страница ${newPage}/${total}\n\n👇 <b>Выбери роль:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("buy_")) {
        const roleName = data.substring(4);
        const result = buyRole(userId, roleName);
        bot.answerCallbackQuery(query.id, { text: result.msg, show_alert: true });
        if (result.success) {
            const role = user.role || "Нет роли";
            const mult = getMultiplier(userId);
            const workshopLevel = user.workshop_level || 1;
            const workshopBonus = getWorkshopBonus(workshopLevel);
            const text = `🌟 <b>Role Shop Bot</b>

┌ 👤 <b>${user.first_name}</b>
├ 🎭 Роль: ${role}
├ 📈 Множитель: x${mult.toFixed(1)}
├ 🔧 Мастерская: ${workshopLevel} ур. (+${workshopBonus}%)
├ 💰 Баланс: ${user.coins}💰
├ 📊 Сообщений: ${user.messages}
└ 🔥 Серия: ${user.daily_streak || 0} дн.

👇 <b>Выбери действие:</b>`;
            bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: getMainMenu(userId) });
        }
        return;
    }
    
    // Профиль
    if (data === "profile") {
        const role = user.role || "Нет роли";
        const mult = getMultiplier(userId);
        const workshopLevel = user.workshop_level || 1;
        const workshopBonus = getWorkshopBonus(workshopLevel);
        const maxLots = getWorkshopMaxLots(workshopLevel);
        const text = `👤 <b>Профиль</b>

┌ 📛 Имя: <b>${user.first_name}</b>
├ 🎭 Роль: ${role}
├ 📈 Множитель: x${mult.toFixed(1)}
├ 🔧 Мастерская: ${workshopLevel} ур. (+${workshopBonus}%)
├ 💰 Монет: ${user.coins}💰
├ 📊 Сообщений: ${user.messages}
├ 📅 Сегодня: ${user.messages_today || 0}
├ 🔥 Серия: ${user.daily_streak || 0} дн.
├ 👥 Пригласил: ${user.invites ? user.invites.length : 0}
├ 💸 С рефералов: ${user.referral_earned || 0}💰
├ 💵 Заработано: ${user.total_earned || 0}💰
├ 💸 Потрачено: ${user.total_spent || 0}💰
├ 📦 Лотов на рынке: ${getUserLots(userId).length}/${maxLots}
└ 📅 Регистрация: ${user.registered_at ? user.registered_at.slice(0,10) : '-'}`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: getBackButton() });
        bot.answerCallbackQuery(query.id);
        return;
    }
    
    // Бонус
    if (data === "bonus") {
        const { bonus, msg } = getDaily(userId);
        bot.answerCallbackQuery(query.id, { text: msg, show_alert: true });
        if (bonus > 0) {
            const role = user.role || "Нет роли";
            const mult = getMultiplier(userId);
            const workshopLevel = user.workshop_level || 1;
            const workshopBonus = getWorkshopBonus(workshopLevel);
            const text = `🌟 <b>Role Shop Bot</b>

┌ 👤 <b>${user.first_name}</b>
├ 🎭 Роль: ${role}
├ 📈 Множитель: x${mult.toFixed(1)}
├ 🔧 Мастерская: ${workshopLevel} ур. (+${workshopBonus}%)
├ 💰 Баланс: ${user.coins}💰
├ 📊 Сообщений: ${user.messages}
└ 🔥 Серия: ${user.daily_streak || 0} дн.

👇 <b>Выбери действие:</b>`;
            bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: getMainMenu(userId) });
        }
        return;
    }
    
    // Топ
    if (data === "top") {
        const users = loadJSON(USERS_FILE);
        const top = [];
        for (const uid in users) {
            if (!MASTER_IDS.includes(parseInt(uid)) && !users[uid].is_banned) {
                top.push([users[uid].first_name || 'User', users[uid].coins]);
            }
        }
        top.sort((a, b) => b[1] - a[1]);
        const top10 = top.slice(0, 10);
        let text = "🏆 <b>Топ по монетам</b>\n\n";
        for (let i = 0; i < top10.length; i++) {
            const [name, coins] = top10[i];
            if (i === 0) text += `🥇 <b>${name}</b> — ${coins}💰\n`;
            else if (i === 1) text += `🥈 <b>${name}</b> — ${coins}💰\n`;
            else if (i === 2) text += `🥉 <b>${name}</b> — ${coins}💰\n`;
            else text += `${i+1}. ${name} — ${coins}💰\n`;
        }
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: getBackButton() });
        bot.answerCallbackQuery(query.id);
        return;
    }
    
    // Помощь
    if (data === "help") {
        const roles = loadRoles();
        let text = "📚 <b>Помощь</b>\n\n<b>💰 Как заработать?</b>\n• Писать в чат — 1-5💰 × множитель\n• /daily — ежедневный бонус\n• Приглашать друзей — 100💰\n• Покупать роли — увеличивать множитель\n• Улучшать мастерскую — увеличивать бонус\n• Продавать роли на рынке\n\n<b>🎭 Все роли:</b>\n";
        for (const [name, data] of Object.entries(roles)) {
            text += `• ${name}: ${data.price}💰 → x${data.mult}\n`;
        }
        text += "\n<b>🔧 Мастерская</b>\nУлучшай мастерскую за монеты. Каждый уровень даёт +% к доходу и больше слотов на рынке.\n\n<b>💰 Рынок</b>\nПродавай свои роли другим игрокам. Комиссия зависит от цены.\n\n<b>📋 Команды:</b>\n• /startrole — запуск бота\n• /menu — главное меню\n• /daily — бонус";
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: getBackButton() });
        bot.answerCallbackQuery(query.id);
        return;
    }
    
    // Мастерская
    if (data === "workshop") {
        const { markup, level, bonus, maxLots, nextPrice } = getWorkshopMenu(userId);
        let text = `🔧 <b>Мастерская</b>\n\n📊 Уровень: <b>${level}</b>\n📈 Бонус к доходу: +${bonus}%\n📦 Слотов на рынке: ${maxLots}\n\n`;
        if (nextPrice) {
            text += `💰 Стоимость улучшения до ${level+1} уровня: ${nextPrice}💰\n\n🎁 <b>Что даст улучшение:</b>\n• +${getWorkshopBonus(level+1)}% к доходу\n• ${getWorkshopMaxLots(level+1)} слотов на рынке`;
        } else {
            text += "✨ <b>Максимальный уровень достигнут!</b>";
        }
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data === "workshop_upgrade") {
        const result = upgradeWorkshop(userId);
        bot.answerCallbackQuery(query.id, { text: result.msg, show_alert: true });
        if (result.success) {
            const { markup, level, bonus, maxLots, nextPrice } = getWorkshopMenu(userId);
            let text = `🔧 <b>Мастерская</b>\n\n📊 Уровень: <b>${level}</b>\n📈 Бонус к доходу: +${bonus}%\n📦 Слотов на рынке: ${maxLots}\n\n`;
            if (nextPrice) {
                text += `💰 Стоимость улучшения до ${level+1} уровня: ${nextPrice}💰\n\n🎁 <b>Что даст улучшение:</b>\n• +${getWorkshopBonus(level+1)}% к доходу\n• ${getWorkshopMaxLots(level+1)} слотов на рынке`;
            } else {
                text += "✨ <b>Максимальный уровень достигнут!</b>";
            }
            bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        }
        return;
    }
    
    // Рынок
    if (data === "market") {
        cleanupExpiredLots();
        const { markup, page, total } = getMarketMenu(1);
        const text = `💰 <b>Рынок ролей</b>\n\n📄 Страница ${page}/${total}\n\n👇 <b>Выбери лот:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("market_page_")) {
        const page = parseInt(data.split('_')[2]);
        const { markup, page: newPage, total } = getMarketMenu(page);
        const text = `💰 <b>Рынок ролей</b>\n\n📄 Страница ${newPage}/${total}\n\n👇 <b>Выбери лот:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("lot_")) {
        const lotId = parseInt(data.split('_')[1]);
        const market = loadMarket();
        const lot = market.lots.find(l => l.id === lotId);
        if (lot) {
            const commission = getMarketCommission(lot.price);
            const commissionAmount = Math.floor(lot.price * commission / 100);
            const text = `🔨 <b>Лот #${lot.id}</b>

🎭 Роль: ${lot.role_name}
💰 Цена: ${lot.price}💰
👤 Продавец: ${lot.seller_username ? `@${lot.seller_username}` : lot.seller_name}
📅 Создан: ${new Date(lot.created_at).toLocaleString().slice(0,16)}

💸 Комиссия: ${commission}% (${commissionAmount}💰)
💰 Продавец получит: ${lot.price - commissionAmount}💰`;
            const markup = {
                inline_keyboard: [
                    [{ text: "✅ Купить", callback_data: `buy_lot_${lotId}` }],
                    [{ text: "◀️ Назад", callback_data: "market" }]
                ]
            };
            bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        }
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("buy_lot_")) {
        const lotId = parseInt(data.split('_')[2]);
        const result = buyMarketLot(lotId, userId);
        bot.answerCallbackQuery(query.id, { text: result.msg, show_alert: true });
        if (result.success) {
            const role = user.role || "Нет роли";
            const mult = getMultiplier(userId);
            const workshopLevel = user.workshop_level || 1;
            const workshopBonus = getWorkshopBonus(workshopLevel);
            const text = `🌟 <b>Role Shop Bot</b>

┌ 👤 <b>${user.first_name}</b>
├ 🎭 Роль: ${role}
├ 📈 Множитель: x${mult.toFixed(1)}
├ 🔧 Мастерская: ${workshopLevel} ур. (+${workshopBonus}%)
├ 💰 Баланс: ${user.coins}💰
├ 📊 Сообщений: ${user.messages}
└ 🔥 Серия: ${user.daily_streak || 0} дн.

👇 <b>Выбери действие:</b>`;
            bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: getMainMenu(userId) });
        }
        return;
    }
    if (data === "market_sell") {
        const userRole = user.role;
        if (!userRole) {
            bot.answerCallbackQuery(query.id, { text: "У вас нет роли для продажи", show_alert: true });
            return;
        }
        bot.sendMessage(userId, `💰 <b>Продажа роли</b>\n\nВаша роль: ${userRole}\n\nВведите цену продажи (мин. ${getMarketMinPrice(userRole)}💰):`, { parse_mode: 'HTML' });
        bot.once('message', (msg) => {
            if (msg.from.id !== userId) return;
            const price = parseInt(msg.text);
            if (isNaN(price)) {
                bot.sendMessage(userId, "❌ Введите число", { parse_mode: 'HTML' });
                return;
            }
            const minPrice = getMarketMinPrice(userRole);
            if (price < minPrice) {
                bot.sendMessage(userId, `❌ Минимальная цена для этой роли: ${minPrice}💰`, { parse_mode: 'HTML' });
                return;
            }
            const result = addMarketLot(userId, userRole, price);
            bot.sendMessage(userId, result.msg, { parse_mode: 'HTML' });
            if (result.success) {
                const role = user.role || "Нет роли";
                const mult = getMultiplier(userId);
                const workshopLevel = user.workshop_level || 1;
                const workshopBonus = getWorkshopBonus(workshopLevel);
                const text = `🌟 <b>Role Shop Bot</b>

┌ 👤 <b>${user.first_name}</b>
├ 🎭 Роль: ${role}
├ 📈 Множитель: x${mult.toFixed(1)}
├ 🔧 Мастерская: ${workshopLevel} ур. (+${workshopBonus}%)
├ 💰 Баланс: ${user.coins}💰
├ 📊 Сообщений: ${user.messages}
└ 🔥 Серия: ${user.daily_streak || 0} дн.

👇 <b>Выбери действие:</b>`;
                bot.sendMessage(userId, text, { parse_mode: 'HTML', reply_markup: getMainMenu(userId) });
            }
        });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data === "market_my_lots") {
        const lots = getUserLots(userId);
        if (lots.length === 0) {
            bot.answerCallbackQuery(query.id, { text: "У вас нет активных лотов", show_alert: true });
            return;
        }
        let text = "📦 <b>Ваши лоты</b>\n\n";
        for (const lot of lots) {
            text += `┌ #${lot.id} — ${lot.role_name}\n├ 💰 ${lot.price}💰\n└ 📅 ${new Date(lot.created_at).toLocaleString().slice(0,16)}\n\n`;
        }
        const markup = { inline_keyboard: [] };
        for (const lot of lots) {
            markup.inline_keyboard.push([{ text: `🗑 Снять лот #${lot.id}`, callback_data: `remove_lot_${lot.id}` }]);
        }
        markup.inline_keyboard.push([{ text: "◀️ Назад", callback_data: "market" }]);
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("remove_lot_")) {
        const lotId = parseInt(data.split('_')[2]);
        const result = removeMarketLot(lotId, userId);
        bot.answerCallbackQuery(query.id, { text: result.msg, show_alert: true });
        cleanupExpiredLots();
        const { markup, page, total } = getMarketMenu(1);
        const text = `💰 <b>Рынок ролей</b>\n\n📄 Страница ${page}/${total}\n\n👇 <b>Выбери лот:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        return;
    }
    
    // Обратная связь
    if (data === "feedback") {
        bot.editMessageText("📝 <b>Обратная связь</b>\n\nВыберите тип сообщения:", { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: getFeedbackMenu() });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data === "send_report") {
        bot.editMessageText("🐞 <b>Отправить отчёт</b>\n\nОпишите проблему. Можно прикрепить фото.\n\nОтправьте сообщение:", { chat_id: chatId, message_id: messageId, parse_mode: 'HTML' });
        bot.once('message', (msg) => {
            if (msg.from.id !== userId) return;
            const text = msg.text || "Без текста";
            const user = getUser(userId);
            saveReport(userId, user.username, user.first_name, text);
            bot.sendMessage(userId, "✅ <b>Отчёт отправлен!</b> Спасибо за помощь.", { parse_mode: 'HTML' });
            const role = user.role || "Нет роли";
            const mult = getMultiplier(userId);
            const workshopLevel = user.workshop_level || 1;
            const workshopBonus = getWorkshopBonus(workshopLevel);
            const menuText = `🌟 <b>Role Shop Bot</b>

┌ 👤 <b>${user.first_name}</b>
├ 🎭 Роль: ${role}
├ 📈 Множитель: x${mult.toFixed(1)}
├ 🔧 Мастерская: ${workshopLevel} ур. (+${workshopBonus}%)
├ 💰 Баланс: ${user.coins}💰
├ 📊 Сообщений: ${user.messages}
└ 🔥 Серия: ${user.daily_streak || 0} дн.

👇 <b>Выбери действие:</b>`;
            bot.sendMessage(userId, menuText, { parse_mode: 'HTML', reply_markup: getMainMenu(userId) });
        });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data === "send_idea") {
        bot.editMessageText("💡 <b>Отправить идею</b>\n\nНапишите вашу идею по улучшению бота.\n\nОтправьте сообщение:", { chat_id: chatId, message_id: messageId, parse_mode: 'HTML' });
        bot.once('message', (msg) => {
            if (msg.from.id !== userId) return;
            const text = msg.text || "Без текста";
            const user = getUser(userId);
            saveIdea(userId, user.username, user.first_name, text);
            bot.sendMessage(userId, "✅ <b>Идея отправлена!</b> Спасибо за вклад.", { parse_mode: 'HTML' });
            const role = user.role || "Нет роли";
            const mult = getMultiplier(userId);
            const workshopLevel = user.workshop_level || 1;
            const workshopBonus = getWorkshopBonus(workshopLevel);
            const menuText = `🌟 <b>Role Shop Bot</b>

┌ 👤 <b>${user.first_name}</b>
├ 🎭 Роль: ${role}
├ 📈 Множитель: x${mult.toFixed(1)}
├ 🔧 Мастерская: ${workshopLevel} ур. (+${workshopBonus}%)
├ 💰 Баланс: ${user.coins}💰
├ 📊 Сообщений: ${user.messages}
└ 🔥 Серия: ${user.daily_streak || 0} дн.

👇 <b>Выбери действие:</b>`;
            bot.sendMessage(userId, menuText, { parse_mode: 'HTML', reply_markup: getMainMenu(userId) });
        });
        bot.answerCallbackQuery(query.id);
        return;
    }
    
    // Админ панель
    if (data === "admin_panel") {
        if (!isAdmin(userId)) {
            bot.answerCallbackQuery(query.id, { text: "Нет доступа", show_alert: true });
            return;
        }
        const text = `🔧 <b>Админ панель</b>\n\n👑 <b>${user.first_name}</b>\n📊 Статус: ${isMaster(userId) ? 'Владелец' : 'Администратор'}\n\n👇 <b>Выбери действие:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: getAdminPanel() });
        bot.answerCallbackQuery(query.id);
        return;
    }
    
    // Админ: статистика
    if (data === "admin_stats") {
        if (!isAdmin(userId)) return;
        const s = getStats();
        const market = loadMarket();
        const text = `📊 <b>Статистика бота</b>\n\n┌ 👥 Пользователей: ${s.total}\n├ 💰 Всего монет: ${s.coins.toLocaleString()}\n├ 💬 Сообщений: ${s.msgs.toLocaleString()}\n├ 🎭 С ролью: ${s.with_role}\n├ 🚫 Забанено: ${s.banned}\n├ ✅ Активных сегодня: ${s.active}\n├ 🎯 Доступно ролей: ${Object.keys(loadRoles()).length}\n├ 🛒 Активных лотов: ${market.lots.length}\n├ 📝 Отчётов: ${getReportsList().length}\n└ 💡 Идей: ${getIdeasList().length}`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: getAdminPanel() });
        bot.answerCallbackQuery(query.id);
        return;
    }
    
    // Админ: пользователи
    if (data === "admin_users") {
        if (!isAdmin(userId)) return;
        const { markup, page, total } = getUsersListMenu(1);
        const text = `👥 <b>Список пользователей</b>\n\n📄 Страница ${page}/${total}\n\n👇 <b>Выбери пользователя:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("users_page_")) {
        const page = parseInt(data.split('_')[2]);
        const { markup, page: newPage, total } = getUsersListMenu(page);
        const text = `👥 <b>Список пользователей</b>\n\n📄 Страница ${newPage}/${total}\n\n👇 <b>Выбери пользователя:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("user_")) {
        const targetId = parseInt(data.split('_')[1]);
        const target = getUser(targetId);
        if (target) {
            const name = target.first_name || 'User';
            const text = `👤 <b>${name}</b>\n\n💰 Баланс: ${target.coins}💰\n🎭 Роль: ${target.role || 'Нет'}\n📊 Сообщений: ${target.messages || 0}\n🚫 Бан: ${target.is_banned ? 'Да' : 'Нет'}\n🔧 Мастерская: ${target.workshop_level || 1} ур.`;
            bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: getUserActionsMenu(targetId) });
        }
        bot.answerCallbackQuery(query.id);
        return;
    }
    
    // Админ: управление рынком
    if (data === "admin_market") {
        if (!isAdmin(userId)) return;
        cleanupExpiredLots();
        const { markup, page, total } = getMarketAdminMenu(1);
        const text = `🛒 <b>Управление рынком</b>\n\n📄 Страница ${page}/${total}\n\n👇 <b>Выбери лот для управления:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("admin_lots_page_")) {
        const page = parseInt(data.split('_')[3]);
        const { markup, page: newPage, total } = getMarketAdminMenu(page);
        const text = `🛒 <b>Управление рынком</b>\n\n📄 Страница ${newPage}/${total}\n\n👇 <b>Выбери лот для управления:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("admin_lot_")) {
        const lotId = parseInt(data.split('_')[2]);
        const market = loadMarket();
        const lot = market.lots.find(l => l.id === lotId);
        if (lot) {
            const text = `🔨 <b>Лот #${lot.id}</b>\n\n🎭 Роль: ${lot.role_name}\n💰 Цена: ${lot.price}💰\n👤 Продавец: ${lot.seller_username ? `@${lot.seller_username}` : lot.seller_name} (ID: ${lot.seller_id})\n📅 Создан: ${new Date(lot.created_at).toLocaleString().slice(0,16)}\n📅 Истекает: ${new Date(lot.expires_at).toLocaleString().slice(0,16)}`;
            const markup = {
                inline_keyboard: [
                    [{ text: "🗑 Удалить лот", callback_data: `admin_del_lot_${lotId}` }],
                    [{ text: "◀️ Назад", callback_data: "admin_market" }]
                ]
            };
            bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        }
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("admin_del_lot_")) {
        const lotId = parseInt(data.split('_')[3]);
        const market = loadMarket();
        const lotIndex = market.lots.findIndex(l => l.id === lotId);
        if (lotIndex !== -1) {
            const lot = market.lots[lotIndex];
            const users = loadJSON(USERS_FILE);
            users[lot.seller_id].role = lot.role_name;
            saveJSON(USERS_FILE, users);
            market.lots.splice(lotIndex, 1);
            saveMarket(market);
            bot.answerCallbackQuery(query.id, { text: `Лот #${lotId} удалён, роль возвращена`, show_alert: true });
        }
        const { markup, page, total } = getMarketAdminMenu(1);
        const text = `🛒 <b>Управление рынком</b>\n\n📄 Страница ${page}/${total}\n\n👇 <b>Выбери лот для управления:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        return;
    }
    
    // Админ: мастерская (настройки)
    if (data === "admin_workshop") {
        if (!isAdmin(userId)) return;
        const settings = loadJSON(SETTINGS_FILE);
        const levels = settings.workshop_levels || {
            1: { price: 0, bonus: 0, max_lots: 1 },
            2: { price: 5000, bonus: 5, max_lots: 1 },
            3: { price: 10000, bonus: 10, max_lots: 2 },
            4: { price: 20000, bonus: 15, max_lots: 2 },
            5: { price: 35000, bonus: 20, max_lots: 3 },
            6: { price: 55000, bonus: 25, max_lots: 3 },
            7: { price: 80000, bonus: 30, max_lots: 4 },
            8: { price: 110000, bonus: 35, max_lots: 4 },
            9: { price: 150000, bonus: 40, max_lots: 5 },
            10: { price: 200000, bonus: 50, max_lots: 5 }
        };
        let text = "🔧 <b>Настройки мастерской</b>\n\n";
        for (const [level, info] of Object.entries(levels)) {
            text += `Уровень ${level}: ${info.price}💰 → +${info.bonus}%, ${info.max_lots} лотов\n`;
        }
        const markup = { inline_keyboard: [[{ text: "◀️ Назад", callback_data: "admin_panel" }]] };
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        bot.answerCallbackQuery(query.id);
        return;
    }
    
    // Админ: отчёты
    if (data === "admin_reports") {
        if (!isAdmin(userId)) return;
        const { markup, page, total } = getReportsListMenu(1);
        const text = `📝 <b>Список отчётов</b>\n\n📄 Страница ${page}/${total}\n\n👇 <b>Выбери отчёт:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("reports_page_")) {
        const page = parseInt(data.split('_')[2]);
        const { markup, page: newPage, total } = getReportsListMenu(page);
        const text = `📝 <b>Список отчётов</b>\n\n📄 Страница ${newPage}/${total}\n\n👇 <b>Выбери отчёт:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("report_")) {
        const reportId = parseInt(data.split('_')[1]);
        const reports = getReportsList();
        const report = reports.find(r => r.id === reportId);
        if (report) {
            const statusText = report.status === 'new' ? "🔴 Новый" : "🟢 Решён";
            const text = `📋 <b>Отчёт #${report.id}</b>\n\n👤 От: ${report.first_name || `User_${report.user_id}`}\n🆔 ID: ${report.user_id}\n📅 Дата: ${new Date(report.created_at).toLocaleString().slice(0,16)}\n📊 Статус: ${statusText}\n\n📝 Сообщение:\n${report.text}`;
            const markup = { inline_keyboard: [] };
            if (report.status === 'new') {
                markup.inline_keyboard.push([{ text: "✅ Отметить решённым", callback_data: `report_resolve_${reportId}` }]);
            }
            markup.inline_keyboard.push([{ text: "🗑 Удалить", callback_data: `report_delete_${reportId}` }]);
            markup.inline_keyboard.push([{ text: "◀️ Назад", callback_data: "admin_reports" }]);
            bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        }
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("report_resolve_")) {
        if (!isAdmin(userId)) return;
        const reportId = parseInt(data.split('_')[2]);
        updateReportStatus(reportId, 'resolved');
        bot.answerCallbackQuery(query.id, { text: "Отмечено как решённое", show_alert: true });
        const { markup, page, total } = getReportsListMenu(1);
        const text = `📝 <b>Список отчётов</b>\n\n📄 Страница ${page}/${total}\n\n👇 <b>Выбери отчёт:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        return;
    }
    if (data.startsWith("report_delete_")) {
        if (!isAdmin(userId)) return;
        const reportId = parseInt(data.split('_')[2]);
        deleteReport(reportId);
        bot.answerCallbackQuery(query.id, { text: "Отчёт удалён", show_alert: true });
        const { markup, page, total } = getReportsListMenu(1);
        const text = `📝 <b>Список отчётов</b>\n\n📄 Страница ${page}/${total}\n\n👇 <b>Выбери отчёт:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        return;
    }
    
    // Админ: идеи
    if (data === "admin_ideas") {
        if (!isAdmin(userId)) return;
        const { markup, page, total } = getIdeasListMenu(1);
        const text = `💡 <b>Список идей</b>\n\n📄 Страница ${page}/${total}\n\n👇 <b>Выбери идею:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("ideas_page_")) {
        const page = parseInt(data.split('_')[2]);
        const { markup, page: newPage, total } = getIdeasListMenu(page);
        const text = `💡 <b>Список идей</b>\n\n📄 Страница ${newPage}/${total}\n\n👇 <b>Выбери идею:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("idea_")) {
        const ideaId = parseInt(data.split('_')[1]);
        const ideas = getIdeasList();
        const idea = ideas.find(i => i.id === ideaId);
        if (idea) {
            const statusText = idea.status === 'new' ? "🔴 Новая" : "🟢 Рассмотрена";
            const text = `💡 <b>Идея #${idea.id}</b>\n\n👤 От: ${idea.first_name || `User_${idea.user_id}`}\n🆔 ID: ${idea.user_id}\n📅 Дата: ${new Date(idea.created_at).toLocaleString().slice(0,16)}\n📊 Статус: ${statusText}\n\n📝 Идея:\n${idea.text}`;
            const markup = { inline_keyboard: [] };
            if (idea.status === 'new') {
                markup.inline_keyboard.push([{ text: "✅ Отметить рассмотренной", callback_data: `idea_consider_${ideaId}` }]);
            }
            markup.inline_keyboard.push([{ text: "🗑 Удалить", callback_data: `idea_delete_${ideaId}` }]);
            markup.inline_keyboard.push([{ text: "◀️ Назад", callback_data: "admin_ideas" }]);
            bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        }
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("idea_consider_")) {
        if (!isAdmin(userId)) return;
        const ideaId = parseInt(data.split('_')[2]);
        updateIdeaStatus(ideaId, 'considered');
        bot.answerCallbackQuery(query.id, { text: "Отмечено как рассмотренное", show_alert: true });
        const { markup, page, total } = getIdeasListMenu(1);
        const text = `💡 <b>Список идей</b>\n\n📄 Страница ${page}/${total}\n\n👇 <b>Выбери идею:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        return;
    }
    if (data.startsWith("idea_delete_")) {
        if (!isAdmin(userId)) return;
        const ideaId = parseInt(data.split('_')[2]);
        deleteIdea(ideaId);
        bot.answerCallbackQuery(query.id, { text: "Идея удалена", show_alert: true });
        const { markup, page, total } = getIdeasListMenu(1);
        const text = `💡 <b>Список идей</b>\n\n📄 Страница ${page}/${total}\n\n👇 <b>Выбери идею:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        return;
    }
    
    // Админ: остальные функции (длинные, упростим для краткости)
    const adminHandlers = [
        'admin_add_coins', 'admin_remove_coins', 'admin_give_role', 'admin_add_role',
        'admin_edit_role', 'admin_del_role', 'admin_list_roles', 'admin_ban', 'admin_unban',
        'admin_add_admin', 'admin_remove_admin', 'admin_mail', 'admin_promo', 'admin_backup',
        'user_add_coins_', 'user_remove_coins_', 'user_give_role_', 'user_ban_', 'user_unban_'
    ];
    
    for (const handler of adminHandlers) {
        if (data === handler || data.startsWith(handler)) {
            if (!isAdmin(userId)) {
                bot.answerCallbackQuery(query.id, { text: "Нет доступа", show_alert: true });
                return;
            }
            if (data === "admin_add_coins") {
                bot.sendMessage(userId, "💰 <b>Выдать монеты</b>\n\nФормат: ID СУММА\n\nПример: 123456789 500", { parse_mode: 'HTML' });
                bot.once('message', (msg) => {
                    if (msg.from.id !== userId) return;
                    const parts = msg.text.split(' ');
                    const target = parseInt(parts[0]);
                    const amount = parseInt(parts[1]);
                    if (isNaN(target) || isNaN(amount)) {
                        bot.sendMessage(userId, "❌ Ошибка! Формат: ID СУММА", { parse_mode: 'HTML' });
                        return;
                    }
                    addCoins(target, amount);
                    bot.sendMessage(userId, `✅ Готово! +${amount}💰 пользователю ${target}`, { parse_mode: 'HTML' });
                    bot.sendMessage(userId, "🔧 Админ панель", { reply_markup: getAdminPanel() });
                });
            } else if (data === "admin_remove_coins") {
                bot.sendMessage(userId, "💸 <b>Забрать монеты</b>\n\nФормат: ID СУММА\n\nПример: 123456789 500", { parse_mode: 'HTML' });
                bot.once('message', (msg) => {
                    if (msg.from.id !== userId) return;
                    const parts = msg.text.split(' ');
                    const target = parseInt(parts[0]);
                    const amount = parseInt(parts[1]);
                    if (isNaN(target) || isNaN(amount)) {
                        bot.sendMessage(userId, "❌ Ошибка! Формат: ID СУММА", { parse_mode: 'HTML' });
                        return;
                    }
                    removeCoins(target, amount);
                    bot.sendMessage(userId, `✅ Готово! -${amount}💰 пользователю ${target}`, { parse_mode: 'HTML' });
                    bot.sendMessage(userId, "🔧 Админ панель", { reply_markup: getAdminPanel() });
                });
            } else if (data === "admin_give_role") {
                const rolesList = Object.keys(loadRoles()).join('\n');
                bot.sendMessage(userId, `🎭 <b>Выдать роль</b>\n\nФормат: ID РОЛЬ\n\nДоступные роли:\n${rolesList}\n\nПример: 123456789 Vip`, { parse_mode: 'HTML' });
                bot.once('message', (msg) => {
                    if (msg.from.id !== userId) return;
                    const parts = msg.text.split(' ');
                    const target = parseInt(parts[0]);
                    const role = parts[1];
                    const roles = loadRoles();
                    if (isNaN(target) || !roles[role]) {
                        bot.sendMessage(userId, "❌ Ошибка! Роль не найдена", { parse_mode: 'HTML' });
                        return;
                    }
                    const users = loadJSON(USERS_FILE);
                    users[target].role = role;
                    saveJSON(USERS_FILE, users);
                    bot.sendMessage(userId, `✅ Готово! Роль ${role} выдана пользователю ${target}`, { parse_mode: 'HTML' });
                    bot.sendMessage(userId, "🔧 Админ панель", { reply_markup: getAdminPanel() });
                });
            } else if (data === "admin_add_role") {
                bot.sendMessage(userId, "➕ <b>Создать роль</b>\n\nФормат: НАЗВАНИЕ ЦЕНА МНОЖИТЕЛЬ\n\nПример: Legend 50000 2.0", { parse_mode: 'HTML' });
                bot.once('message', (msg) => {
                    if (msg.from.id !== userId) return;
                    const parts = msg.text.split(' ');
                    const name = parts[0];
                    const price = parseInt(parts[1]);
                    const mult = parseFloat(parts[2]);
                    if (!name || isNaN(price) || isNaN(mult)) {
                        bot.sendMessage(userId, "❌ Ошибка! Формат: НАЗВАНИЕ ЦЕНА МНОЖИТЕЛЬ", { parse_mode: 'HTML' });
                        return;
                    }
                    const roles = loadRoles();
                    if (roles[name]) {
                        bot.sendMessage(userId, `❌ Роль ${name} уже существует`, { parse_mode: 'HTML' });
                        return;
                    }
                    roles[name] = { price, mult };
                    saveRoles(roles);
                    bot.sendMessage(userId, `✅ Роль ${name} создана!`, { parse_mode: 'HTML' });
                    bot.sendMessage(userId, "🔧 Админ панель", { reply_markup: getAdminPanel() });
                });
            } else if (data === "admin_edit_role") {
                bot.sendMessage(userId, "✏️ <b>Редактировать роль</b>\n\nФормат: НАЗВАНИЕ ЦЕНА МНОЖИТЕЛЬ\n\nИспользуйте - чтобы не менять\nПример: Vip 15000 -", { parse_mode: 'HTML' });
                bot.once('message', (msg) => {
                    if (msg.from.id !== userId) return;
                    const parts = msg.text.split(' ');
                    const name = parts[0];
                    const roles = loadRoles();
                    if (!roles[name]) {
                        bot.sendMessage(userId, `❌ Роль ${name} не найдена`, { parse_mode: 'HTML' });
                        return;
                    }
                    const oldPrice = roles[name].price;
                    const oldMult = roles[name].mult;
                    const price = parts[1] !== '-' ? parseInt(parts[1]) : oldPrice;
                    const mult = parts[2] !== '-' ? parseFloat(parts[2]) : oldMult;
                    roles[name] = { price, mult };
                    saveRoles(roles);
                    bot.sendMessage(userId, `✅ Роль ${name} обновлена! Цена: ${price} (было ${oldPrice}), множитель: x${mult} (было x${oldMult})`, { parse_mode: 'HTML' });
                    bot.sendMessage(userId, "🔧 Админ панель", { reply_markup: getAdminPanel() });
                });
            } else if (data === "admin_del_role") {
                const rolesList = Object.keys(loadRoles()).join('\n');
                bot.sendMessage(userId, `🗑 <b>Удалить роль</b>\n\nФормат: НАЗВАНИЕ\n\nДоступные роли:\n${rolesList}\n\nПример: Legend\n\n⚠️ У пользователей с этой ролью она пропадёт`, { parse_mode: 'HTML' });
                bot.once('message', (msg) => {
                    if (msg.from.id !== userId) return;
                    const name = msg.text.trim();
                    const roles = loadRoles();
                    if (!roles[name]) {
                        bot.sendMessage(userId, `❌ Роль ${name} не найдена`, { parse_mode: 'HTML' });
                        return;
                    }
                    const users = loadJSON(USERS_FILE);
                    let removed = 0;
                    for (const uid in users) {
                        if (users[uid].role === name) {
                            users[uid].role = null;
                            removed++;
                        }
                    }
                    delete roles[name];
                    saveRoles(roles);
                    saveJSON(USERS_FILE, users);
                    bot.sendMessage(userId, `✅ Роль ${name} удалена! У ${removed} пользователей роль сброшена`, { parse_mode: 'HTML' });
                    bot.sendMessage(userId, "🔧 Админ панель", { reply_markup: getAdminPanel() });
                });
            } else if (data === "admin_list_roles") {
                const roles = loadRoles();
                let text = "📋 <b>Список ролей</b>\n\n";
                for (const [name, data] of Object.entries(roles)) {
                    text += `┌ <b>${name}</b>\n├ 💰 Цена: ${data.price}💰\n└ 📈 Множитель: x${data.mult}\n\n`;
                }
                text += `📊 <b>Всего ролей:</b> ${Object.keys(roles).length}`;
                bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: getAdminPanel() });
            } else if (data === "admin_ban") {
                bot.sendMessage(userId, "🚫 <b>Забанить</b>\n\nФормат: ID ПРИЧИНА\n\nПример: 123456789 Спам", { parse_mode: 'HTML' });
                bot.once('message', (msg) => {
                    if (msg.from.id !== userId) return;
                    const parts = msg.text.split(' ');
                    const target = parseInt(parts[0]);
                    const reason = parts.slice(1).join(' ') || "Не указана";
                    const users = loadJSON(USERS_FILE);
                    if (!users[target]) {
                        bot.sendMessage(userId, "❌ Пользователь не найден", { parse_mode: 'HTML' });
                        return;
                    }
                    users[target].is_banned = true;
                    users[target].ban_reason = reason;
                    saveJSON(USERS_FILE, users);
                    bot.sendMessage(userId, `✅ Пользователь ${target} забанен\nПричина: ${reason}`, { parse_mode: 'HTML' });
                    try {
                        bot.sendMessage(target, `🚫 <b>Вы забанены!</b>\n\nПричина: ${reason}`, { parse_mode: 'HTML' });
                    } catch(e) {}
                    bot.sendMessage(userId, "🔧 Админ панель", { reply_markup: getAdminPanel() });
                });
            } else if (data === "admin_unban") {
                bot.sendMessage(userId, "✅ <b>Разбанить</b>\n\nФормат: ID\n\nПример: 123456789", { parse_mode: 'HTML' });
                bot.once('message', (msg) => {
                    if (msg.from.id !== userId) return;
                    const target = parseInt(msg.text);
                    const users = loadJSON(USERS_FILE);
                    if (!users[target]) {
                        bot.sendMessage(userId, "❌ Пользователь не найден", { parse_mode: 'HTML' });
                        return;
                    }
                    users[target].is_banned = false;
                    users[target].ban_reason = null;
                    saveJSON(USERS_FILE, users);
                    bot.sendMessage(userId, `✅ Пользователь ${target} разбанен`, { parse_mode: 'HTML' });
                    try {
                        bot.sendMessage(target, `✅ <b>Вы разбанены!</b>`, { parse_mode: 'HTML' });
                    } catch(e) {}
                    bot.sendMessage(userId, "🔧 Админ панель", { reply_markup: getAdminPanel() });
                });
            } else if (data === "admin_add_admin") {
                if (!isMaster(userId)) {
                    bot.answerCallbackQuery(query.id, { text: "Только для владельца", show_alert: true });
                    return;
                }
                bot.sendMessage(userId, "👑 <b>Добавить админа</b>\n\nФормат: ID\n\nПример: 123456789", { parse_mode: 'HTML' });
                bot.once('message', (msg) => {
                    if (msg.from.id !== userId) return;
                    const target = parseInt(msg.text);
                    const admins = loadJSON(path.join(DATA_DIR, 'admins.json'));
                    if (!admins.admin_list) admins.admin_list = {};
                    admins.admin_list[target] = { level: 'moderator', added_by: userId, added_at: formatDate(getMoscowTime()) };
                    saveJSON(path.join(DATA_DIR, 'admins.json'), admins);
                    bot.sendMessage(userId, `✅ Пользователь ${target} назначен администратором`, { parse_mode: 'HTML' });
                    try {
                        bot.sendMessage(target, `👑 <b>Вы стали администратором!</b>`, { parse_mode: 'HTML' });
                    } catch(e) {}
                    bot.sendMessage(userId, "🔧 Админ панель", { reply_markup: getAdminPanel() });
                });
            } else if (data === "admin_remove_admin") {
                if (!isMaster(userId)) {
                    bot.answerCallbackQuery(query.id, { text: "Только для владельца", show_alert: true });
                    return;
                }
                bot.sendMessage(userId, "🗑 <b>Удалить админа</b>\n\nФормат: ID\n\nПример: 123456789", { parse_mode: 'HTML' });
                bot.once('message', (msg) => {
                    if (msg.from.id !== userId) return;
                    const target = parseInt(msg.text);
                    if (MASTER_IDS.includes(target)) {
                        bot.sendMessage(userId, "❌ Нельзя удалить владельца", { parse_mode: 'HTML' });
                        return;
                    }
                    const admins = loadJSON(path.join(DATA_DIR, 'admins.json'));
                    if (admins.admin_list && admins.admin_list[target]) {
                        delete admins.admin_list[target];
                        saveJSON(path.join(DATA_DIR, 'admins.json'), admins);
                        bot.sendMessage(userId, `✅ Администратор ${target} удалён`, { parse_mode: 'HTML' });
                        try {
                            bot.sendMessage(target, `🗑 <b>Вы были удалены из админов</b>`, { parse_mode: 'HTML' });
                        } catch(e) {}
                    } else {
                        bot.sendMessage(userId, `❌ Пользователь ${target} не является администратором`, { parse_mode: 'HTML' });
                    }
                    bot.sendMessage(userId, "🔧 Админ панель", { reply_markup: getAdminPanel() });
                });
            } else if (data === "admin_mail") {
                bot.sendMessage(userId, "📢 <b>Рассылка</b>\n\nОтправьте сообщение для рассылки всем пользователям:", { parse_mode: 'HTML' });
                bot.once('message', (msg) => {
                    if (msg.from.id !== userId) return;
                    const users = loadJSON(USERS_FILE);
                    let sent = 0;
                    for (const uid in users) {
                        if (MASTER_IDS.includes(parseInt(uid))) continue;
                        try {
                            bot.sendMessage(parseInt(uid), `📢 <b>Рассылка от администрации</b>\n\n${msg.text}`, { parse_mode: 'HTML' });
                            sent++;
                        } catch(e) {}
                    }
                    bot.sendMessage(userId, `✅ <b>Рассылка завершена</b>\n\n📤 Отправлено: ${sent}`, { parse_mode: 'HTML' });
                    bot.sendMessage(userId, "🔧 Админ панель", { reply_markup: getAdminPanel() });
                });
            } else if (data === "admin_promo") {
                const text = `🎁 <b>Промокоды</b>\n\n<b>Создать промокод на монеты:</b>\n<code>/createpromo КОД СУММА ЛИМИТ ДНИ</code>\n\n<b>Создать промокод на роль:</b>\n<code>/createrole КОД РОЛЬ ДНИ ЛИМИТ</code>\n\n<b>Примеры:</b>\n<code>/createpromo HELLO 500 10 7</code>\n<code>/createrole VIPPROMO Vip 30 5</code>`;
                bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: getAdminPanel() });
            } else if (data === "admin_backup") {
                if (!isMaster(userId)) {
                    bot.answerCallbackQuery(query.id, { text: "Только для владельца", show_alert: true });
                    return;
                }
                const backupDir = path.join(__dirname, `backup_${getMoscowTime().toISOString().slice(0,19).replace(/:/g, '-')}`);
                if (!fs.existsSync(backupDir)) fs.mkdirSync(backupDir);
                const files = [USERS_FILE, path.join(DATA_DIR, 'admins.json'), PROMO_FILE, ROLES_FILE, MARKET_FILE, REPORTS_FILE, IDEAS_FILE, SETTINGS_FILE];
                for (const file of files) {
                    if (fs.existsSync(file)) {
                        fs.copyFileSync(file, path.join(backupDir, path.basename(file)));
                    }
                }
                bot.sendMessage(userId, `✅ <b>Бэкап создан</b>\n\n📁 Папка: ${backupDir}\n📅 ${formatDate(getMoscowTime())}`, { parse_mode: 'HTML' });
                bot.answerCallbackQuery(query.id);
            }
            bot.answerCallbackQuery(query.id);
            return;
        }
    }
    
    // Действия с пользователями
    if (data.startsWith("user_add_coins_")) {
        const targetId = parseInt(data.split('_')[3]);
        bot.sendMessage(userId, `💰 <b>Выдать монеты</b>\n\nПользователь ID: ${targetId}\n\nВведите сумму:`, { parse_mode: 'HTML' });
        bot.once('message', (msg) => {
            if (msg.from.id !== userId) return;
            const amount = parseInt(msg.text);
            if (isNaN(amount)) {
                bot.sendMessage(userId, "❌ Введите число", { parse_mode: 'HTML' });
                return;
            }
            addCoins(targetId, amount);
            bot.sendMessage(userId, `✅ Готово! +${amount}💰 пользователю ${targetId}`, { parse_mode: 'HTML' });
            bot.sendMessage(userId, "🔧 Админ панель", { reply_markup: getAdminPanel() });
        });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("user_remove_coins_")) {
        const targetId = parseInt(data.split('_')[3]);
        bot.sendMessage(userId, `💸 <b>Забрать монеты</b>\n\nПользователь ID: ${targetId}\n\nВведите сумму:`, { parse_mode: 'HTML' });
        bot.once('message', (msg) => {
            if (msg.from.id !== userId) return;
            const amount = parseInt(msg.text);
            if (isNaN(amount)) {
                bot.sendMessage(userId, "❌ Введите число", { parse_mode: 'HTML' });
                return;
            }
            removeCoins(targetId, amount);
            bot.sendMessage(userId, `✅ Готово! -${amount}💰 пользователю ${targetId}`, { parse_mode: 'HTML' });
            bot.sendMessage(userId, "🔧 Админ панель", { reply_markup: getAdminPanel() });
        });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("user_give_role_")) {
        const targetId = parseInt(data.split('_')[3]);
        const rolesList = Object.keys(loadRoles()).join('\n');
        bot.sendMessage(userId, `🎭 <b>Выдать роль</b>\n\nПользователь ID: ${targetId}\n\nДоступные роли:\n${rolesList}\n\nВведите название роли:`, { parse_mode: 'HTML' });
        bot.once('message', (msg) => {
            if (msg.from.id !== userId) return;
            const role = msg.text.trim();
            const roles = loadRoles();
            if (!roles[role]) {
                bot.sendMessage(userId, `❌ Роль ${role} не найдена`, { parse_mode: 'HTML' });
                return;
            }
            const users = loadJSON(USERS_FILE);
            users[targetId].role = role;
            saveJSON(USERS_FILE, users);
            bot.sendMessage(userId, `✅ Готово! Роль ${role} выдана пользователю ${targetId}`, { parse_mode: 'HTML' });
            bot.sendMessage(userId, "🔧 Админ панель", { reply_markup: getAdminPanel() });
        });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("user_ban_")) {
        const targetId = parseInt(data.split('_')[3]);
        bot.sendMessage(userId, `🚫 <b>Забанить</b>\n\nПользователь ID: ${targetId}\n\nВведите причину бана:`, { parse_mode: 'HTML' });
        bot.once('message', (msg) => {
            if (msg.from.id !== userId) return;
            const reason = msg.text;
            const users = loadJSON(USERS_FILE);
            if (!users[targetId]) {
                bot.sendMessage(userId, "❌ Пользователь не найден", { parse_mode: 'HTML' });
                return;
            }
            users[targetId].is_banned = true;
            users[targetId].ban_reason = reason;
            saveJSON(USERS_FILE, users);
            bot.sendMessage(userId, `✅ Пользователь ${targetId} забанен\nПричина: ${reason}`, { parse_mode: 'HTML' });
            try {
                bot.sendMessage(targetId, `🚫 <b>Вы забанены!</b>\n\nПричина: ${reason}`, { parse_mode: 'HTML' });
            } catch(e) {}
            bot.sendMessage(userId, "🔧 Админ панель", { reply_markup: getAdminPanel() });
        });
        bot.answerCallbackQuery(query.id);
        return;
    }
    if (data.startsWith("user_unban_")) {
        const targetId = parseInt(data.split('_')[3]);
        const users = loadJSON(USERS_FILE);
        if (!users[targetId]) {
            bot.answerCallbackQuery(query.id, { text: "Пользователь не найден", show_alert: true });
            return;
        }
        users[targetId].is_banned = false;
        users[targetId].ban_reason = null;
        saveJSON(USERS_FILE, users);
        bot.answerCallbackQuery(query.id, { text: `Пользователь ${targetId} разбанен`, show_alert: true });
        try {
            bot.sendMessage(targetId, `✅ <b>Вы разбанены!</b>`, { parse_mode: 'HTML' });
        } catch(e) {}
        const { markup, page, total } = getUsersListMenu(1);
        const text = `👥 <b>Список пользователей</b>\n\n📄 Страница ${page}/${total}\n\n👇 <b>Выбери пользователя:</b>`;
        bot.editMessageText(text, { chat_id: chatId, message_id: messageId, parse_mode: 'HTML', reply_markup: markup });
        return;
    }
    
    bot.answerCallbackQuery(query.id);
});

// ========== ПРОМОКОДЫ ==========
bot.onText(/\/createpromo (.+)/, (msg, match) => {
    const userId = msg.from.id;
    if (!isAdmin(userId)) {
        bot.sendMessage(msg.chat.id, "Нет доступа");
        return;
    }
    const parts = match[1].split(' ');
    if (parts.length < 4) {
        bot.sendMessage(msg.chat.id, "❌ /createpromo КОД СУММА ЛИМИТ ДНИ");
        return;
    }
    const code = parts[0].toUpperCase();
    const coins = parseInt(parts[1]);
    const maxUses = parseInt(parts[2]);
    const days = parseInt(parts[3]) || 7;
    const promos = loadJSON(PROMO_FILE);
    promos[code] = {
        type: 'coins',
        coins: coins,
        max_uses: maxUses,
        used: 0,
        used_by: [],
        expires_at: new Date(getMoscowTime().getTime() + days * 24 * 60 * 60 * 1000).toISOString()
    };
    saveJSON(PROMO_FILE, promos);
    bot.sendMessage(msg.chat.id, `✅ <b>Промокод создан</b>\n\nКод: ${code}\nМонеты: ${coins}💰\nЛимит: ${maxUses}\nДней: ${days}`, { parse_mode: 'HTML' });
});

bot.onText(/\/createrole (.+)/, (msg, match) => {
    const userId = msg.from.id;
    if (!isAdmin(userId)) {
        bot.sendMessage(msg.chat.id, "Нет доступа");
        return;
    }
    const parts = match[1].split(' ');
    if (parts.length < 4) {
        bot.sendMessage(msg.chat.id, "❌ /createrole КОД РОЛЬ ДНИ ЛИМИТ");
        return;
    }
    const code = parts[0].toUpperCase();
    const role = parts[1];
    const days = parseInt(parts[2]);
    const maxUses = parseInt(parts[3]);
    const roles = loadRoles();
    if (!roles[role]) {
        bot.sendMessage(msg.chat.id, `❌ Роль ${role} не найдена`);
        return;
    }
    const promos = loadJSON(PROMO_FILE);
    promos[code] = {
        type: 'role',
        role: role,
        days: days,
        max_uses: maxUses,
        used: 0,
        used_by: [],
        expires_at: new Date(getMoscowTime().getTime() + 30 * 24 * 60 * 60 * 1000).toISOString()
    };
    saveJSON(PROMO_FILE, promos);
    bot.sendMessage(msg.chat.id, `✅ <b>Промокод на роль создан</b>\n\nКод: ${code}\nРоль: ${role}\nДней: ${days}\nЛимит: ${maxUses}`, { parse_mode: 'HTML' });
});

bot.onText(/\/use (.+)/, (msg, match) => {
    const chatId = msg.chat.id;
    if (msg.chat.type !== 'private') return;
    const userId = msg.from.id;
    const code = match[1].toUpperCase();
    const promos = loadJSON(PROMO_FILE);
    if (!promos[code]) {
        bot.sendMessage(chatId, "❌ Промокод не найден");
        return;
    }
    const promo = promos[code];
    if (new Date(promo.expires_at) < getMoscowTime()) {
        bot.sendMessage(chatId, "❌ Промокод истёк");
        return;
    }
    if (promo.used >= promo.max_uses) {
        bot.sendMessage(chatId, "❌ Промокод уже использован");
        return;
    }
    if (promo.used_by && promo.used_by.includes(userId.toString())) {
        bot.sendMessage(chatId, "❌ Вы уже использовали этот промокод");
        return;
    }
    if (promo.type === 'coins') {
        addCoins(userId, promo.coins);
        promo.used++;
        if (!promo.used_by) promo.used_by = [];
        promo.used_by.push(userId.toString());
        saveJSON(PROMO_FILE, promos);
        bot.sendMessage(chatId, `✅ <b>Промокод активирован!</b>\n\n+${promo.coins}💰`, { parse_mode: 'HTML' });
    } else if (promo.type === 'role') {
        const users = loadJSON(USERS_FILE);
        users[userId].role = promo.role;
        saveJSON(USERS_FILE, users);
        promo.used++;
        if (!promo.used_by) promo.used_by = [];
        promo.used_by.push(userId.toString());
        saveJSON(PROMO_FILE, promos);
        bot.sendMessage(chatId, `✅ <b>Промокод активирован!</b>\n\nВы получили роль ${promo.role} на ${promo.days} дней`, { parse_mode: 'HTML' });
    }
});

// ========== НАЧИСЛЕНИЕ ЗА СООБЩЕНИЯ ==========
bot.on('message', (msg) => {
    if (msg.chat.type !== 'private' && !msg.from.is_bot) {
        addMessage(msg.from.id);
        checkReferralReward(msg.from.id);
    }
});

// ========== ФОНОВЫЙ ПОТОК ДЛЯ ОЧИСТКИ РЫНКА ==========
setInterval(() => {
    cleanupExpiredLots();
}, 3600000);

console.log('🌟 ROLE SHOP BOT ЗАПУЩЕН');
console.log(`👑 Владелец: ${MASTER_IDS[0]}`);
console.log(`🎭 Доступно ролей: ${Object.keys(loadRoles()).length}`);
console.log('✅ БОТ ГОТОВ К РАБОТЕ!');
console.log('📌 Команда: /startrole');
