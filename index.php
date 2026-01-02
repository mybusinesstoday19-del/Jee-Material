<?php
// index.php

// 1. Load Configuration (Use Environment Variables for security)
// On Render, set BOT_TOKEN in the "Environment" tab.
$token = getenv('BOT_TOKEN') ?: 'YOUR_HARDCODED_TOKEN_FALLBACK'; 
define('BOT_TOKEN', $token);
define('API_URL', 'https://api.telegram.org/bot' . BOT_TOKEN . '/');
define('USERS_FILE', 'users.json');
define('ERROR_LOG', 'error.log');

// 2. Helper Functions
function logError($message) {
    // Write to stderr so it shows up in Render logs
    file_put_contents('php://stderr', date('[Y-m-d H:i:s] ') . $message . "\n");
}

function loadUsers() {
    if (!file_exists(USERS_FILE)) {
        // Initialize with empty array if missing
        file_put_contents(USERS_FILE, json_encode([]));
        return [];
    }
    $content = file_get_contents(USERS_FILE);
    return json_decode($content, true) ?: [];
}

function saveUsers($users) {
    // Atomic write to prevent corruption
    $temp_file = USERS_FILE . '.tmp';
    if (file_put_contents($temp_file, json_encode($users, JSON_PRETTY_PRINT))) {
        rename($temp_file, USERS_FILE);
        return true;
    }
    return false;
}

function sendMessage($chat_id, $text, $keyboard = null) {
    $params = [
        'chat_id' => $chat_id,
        'text' => $text,
        'parse_mode' => 'HTML'
    ];
    if ($keyboard) {
        $params['reply_markup'] = json_encode(['inline_keyboard' => $keyboard]);
    }
    
    $ch = curl_init(API_URL . 'sendMessage');
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $params);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $result = curl_exec($ch);
    curl_close($ch);
    return $result;
}

function getMainKeyboard() {
    return [
        [['text' => '💰 Earn', 'callback_data' => 'earn'], ['text' => '🏦 Balance', 'callback_data' => 'balance']],
        [['text' => '🏆 Leaderboard', 'callback_data' => 'leaderboard'], ['text' => '👥 Referrals', 'callback_data' => 'referrals']],
        [['text' => '💳 Withdraw', 'callback_data' => 'withdraw'], ['text' => '❓ Help', 'callback_data' => 'help']]
    ];
}

function processUpdate($update) {
    $users = loadUsers();
    $save_needed = false;

    if (isset($update['message'])) {
        $chat_id = $update['message']['chat']['id'];
        $text = trim($update['message']['text'] ?? '');

        if (!isset($users[$chat_id])) {
            $users[$chat_id] = [
                'balance' => 0, 'last_earn' => 0, 'referrals' => 0,
                'ref_code' => substr(md5($chat_id . time()), 0, 8), 'referred_by' => null
            ];
            $save_needed = true;
        }

        if (strpos($text, '/start') === 0) {
            $parts = explode(' ', $text);
            $ref = $parts[1] ?? null;
            
            if ($ref && empty($users[$chat_id]['referred_by']) && $ref !== $users[$chat_id]['ref_code']) {
                // Find referrer
                foreach ($users as $id => $user) {
                    if (isset($user['ref_code']) && $user['ref_code'] === $ref) {
                        $users[$chat_id]['referred_by'] = $id;
                        $users[$id]['referrals'] = ($users[$id]['referrals'] ?? 0) + 1;
                        $users[$id]['balance'] = ($users[$id]['balance'] ?? 0) + 50;
                        sendMessage($id, "🎉 New referral! +50 points bonus!");
                        $save_needed = true;
                        break;
                    }
                }
            }
            
            $msg = "Welcome to Earning Bot!\nYour code: <b>{$users[$chat_id]['ref_code']}</b>";
            sendMessage($chat_id, $msg, getMainKeyboard());
        }
    } elseif (isset($update['callback_query'])) {
        $cb = $update['callback_query'];
        $chat_id = $cb['message']['chat']['id'];
        $data = $cb['data'];
        
        // Acknowledge callback to stop loading animation
        file_get_contents(API_URL . "answerCallbackQuery?callback_query_id=" . $cb['id']);

        if (!isset($users[$chat_id])) {
            $users[$chat_id] = [
                'balance' => 0, 'last_earn' => 0, 'referrals' => 0,
                'ref_code' => substr(md5($chat_id . time()), 0, 8), 'referred_by' => null
            ];
            $save_needed = true;
        }

        $msg = "";
        switch ($data) {
            case 'earn':
                $now = time();
                $last = $users[$chat_id]['last_earn'] ?? 0;
                if (($now - $last) < 60) {
                    $msg = "⏳ Wait " . (60 - ($now - $last)) . "s more!";
                } else {
                    $users[$chat_id]['balance'] += 10;
                    $users[$chat_id]['last_earn'] = $now;
                    $msg = "✅ Earned 10 points! Bal: {$users[$chat_id]['balance']}";
                    $save_needed = true;
                }
                break;
            case 'balance':
                $msg = "💰 Points: {$users[$chat_id]['balance']}\n👥 Refs: {$users[$chat_id]['referrals']}";
                break;
            case 'leaderboard':
                 $msg = "🏆 Leaderboard logic here..."; // Simplified for brevity
                 break;
            case 'referrals':
                $bot_username = "YOUR_BOT_USERNAME"; // Optional: fetch dynamically or hardcode
                $msg = "🔗 Link: https://t.me/$bot_username?start={$users[$chat_id]['ref_code']}";
                break;
            case 'withdraw':
                $msg = "💳 Balance: {$users[$chat_id]['balance']}. Min withdraw: 100.";
                break;
            case 'help':
                $msg = "ℹ️ Click Earn every minute.";
                break;
        }
        if ($msg) sendMessage($chat_id, $msg);
    }

    if ($save_needed) {
        saveUsers($users);
    }
}

// 3. Webhook Handling Logic
// Check if this is a request from Telegram
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $content = file_get_contents("php://input");
    $update = json_decode($content, true);
    
    if ($update) {
        processUpdate($update);
    }
    http_response_code(200); // Tell Telegram "OK"
    exit;
} else {
    // If accessed via browser, show status or setup webhook
    echo "Bot is running. <br>";
    echo "To connect to Telegram, run this once locally:<br>";
    echo "<code>curl https://api.telegram.org/bot".BOT_TOKEN."/setWebhook?url=https://YOUR-RENDER-APP-NAME.onrender.com/</code>";
}
?>