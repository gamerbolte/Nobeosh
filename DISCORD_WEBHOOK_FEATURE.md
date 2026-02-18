# Discord Webhook Integration for Order Notifications

## 🎯 Overview

Products can now be configured with Discord webhook URLs to automatically send order notifications to Discord channels. This allows real-time order tracking directly in your Discord server with rich embedded messages.

**Key Features:**
- ✅ Multiple webhooks per product
- ✅ @everyone mentions for instant alerts
- ✅ Rich embed messages with order details
- ✅ Hidden from public API (admin-only access)
- ✅ Automatic notifications on order confirmation
- ✅ Beautiful formatting with Discord embeds

---

## 📱 What Gets Sent to Discord

### Order Notification Embed

When a customer places an order for a product with webhooks configured:

```
@everyone 🔔 New Order Received!

┌─────────────────────────────────────┐
│ ⏳ New Order - #A1B2C3D4            │
│ A new order has been placed!        │
├─────────────────────────────────────┤
│ 👤 Customer Name: John Doe          │
│ 📧 Email: john@example.com          │
│ 📱 Phone: +977 9876543210           │
│                                     │
│ 📦 Order Items:                     │
│ • 1x Netflix Premium (1 Month) -    │
│   Rs 450.00                         │
│ • 2x Spotify Premium (1 Month) -    │
│   Rs 200.00                         │
│                                     │
│ 💰 Total Amount: Rs 850.00          │
│ 📊 Status: ⏳ PENDING               │
│ 🆔 Order ID: a1b2c3d4-...          │
│                                     │
│ 📝 Remarks:                         │
│ Please deliver within 24 hours      │
└─────────────────────────────────────┘

GameShop Nepal - Order Management
```

**Embed Features:**
- Color-coded by status (Orange=Pending, Blue=Processing, Green=Completed, Red=Cancelled)
- Product thumbnail image
- Organized fields with emojis
- Timestamp
- Footer with branding

---

## 🔧 Setup Guide

### Step 1: Create Discord Webhook

1. **Open Discord Server**
2. **Go to Server Settings** → **Integrations** → **Webhooks**
3. **Click "New Webhook"** or "Create Webhook"
4. **Configure Webhook:**
   - Name: "GameShop Orders" (or any name)
   - Channel: Select the channel for notifications
   - Avatar: Optional (set a custom icon)
5. **Copy Webhook URL**
   - Format: `https://discord.com/api/webhooks/{webhook_id}/{webhook_token}`
6. **Save Changes**

### Step 2: Add Webhook to Product

1. **Login to Admin Panel**: `/panelgsnadminbackend/login`
2. **Go to**: Store → Products
3. **Create or Edit** a product
4. **Scroll to**: "🔮 Discord Order Notifications" section
5. **Paste Webhook URL** in the input field
6. **Click "+" button** to add
7. **Add Multiple Webhooks** (optional)
   - Repeat steps 5-6 for additional channels
8. **Save Product**

### Step 3: Test

1. **Place a test order** for the product
2. **Check Discord channel**
3. **You should see** @everyone mention with order embed! 🎉

---

## 🎨 Admin Panel Interface

### Discord Webhook Section

```
┌─────────────────────────────────────────────────┐
│ 🔮 Discord Order Notifications                  │
│ Send order notifications to Discord channels.   │
│ Webhooks are hidden from customers.             │
│                                                  │
│ Discord Webhooks:                                │
│ ┌─────────────────────────────┬────┐           │
│ │ https://discord.com/api/... │ +  │           │
│ └─────────────────────────────┴────┘           │
│ Get webhook URL from Discord: Server Settings   │
│ → Integrations → Webhooks                       │
│                                                  │
│ Active Webhooks (2):                             │
│ ┌─────────────────────────────────────┬─┐       │
│ │ https://discord.com/api/webhooks... │X│       │
│ └─────────────────────────────────────┴─┘       │
│ ┌─────────────────────────────────────┬─┐       │
│ │ https://discord.com/api/webhooks... │X│       │
│ └─────────────────────────────────────┴─┘       │
│                                                  │
│ 📢 Notification Info:                            │
│ • Sends @everyone mention                        │
│ • Triggers on confirmed orders                   │
│ • Includes order details in embed                │
│ • Not visible to customers                       │
└─────────────────────────────────────────────────┘
```

---

## 🔐 Security Features

### Webhooks Hidden from Public

**Backend Protection:**
```python
# Public API removes webhooks
product.pop("discord_webhooks", None)  # Not exposed
```

**What Customers See:**
```json
{
  "id": "product-123",
  "name": "Netflix Premium",
  "price": 450,
  // NO discord_webhooks field
}
```

**What Admins See:**
```json
{
  "id": "product-123",
  "name": "Netflix Premium",
  "price": 450,
  "discord_webhooks": [
    "https://discord.com/api/webhooks/..."
  ]
}
```

**Protected Endpoints:**
- ✅ `/api/products` - Webhooks removed
- ✅ `/api/products/{id}` - Webhooks removed
- ✅ Only admin create/update includes webhooks

---

## 📊 Use Cases

### Use Case 1: Single Channel Notifications
```yaml
Product: Netflix Premium
Webhooks: 
  - https://discord.com/api/webhooks/xxx (Sales channel)
Result: All Netflix orders → #sales channel
```

### Use Case 2: Multi-Channel Notifications
```yaml
Product: PUBG UC - Bulk Package
Webhooks:
  - https://discord.com/api/webhooks/xxx (Sales channel)
  - https://discord.com/api/webhooks/yyy (Management channel)
  - https://discord.com/api/webhooks/zzz (Inventory channel)
Result: All PUBG bulk orders → 3 channels simultaneously
```

### Use Case 3: Category-Based Routing
```yaml
Product 1: Gaming Gift Cards
Webhooks: [Gaming channel webhook]

Product 2: Streaming Services
Webhooks: [Streaming channel webhook]

Result: Orders routed to specific Discord channels
```

### Use Case 4: Priority Alerts
```yaml
Product: High-Value Custom PC Build
Webhooks: [VIP-Orders channel webhook]
Result: High-value orders get special attention
```

---

## 🎨 Embed Customization

### Status Colors

| Status | Color | Hex Code |
|--------|-------|----------|
| Pending | 🟠 Orange | #FFA500 |
| Processing | 🔵 Blue | #3498DB |
| Completed | 🟢 Green | #2ECC71 |
| Cancelled | 🔴 Red | #E74C3C |

### Status Emojis

| Status | Emoji |
|--------|-------|
| Pending | ⏳ |
| Processing | 🔄 |
| Completed | ✅ |
| Cancelled | ❌ |

---

## 🔄 Workflow

### Order Creation Flow

```
Customer Places Order
         ↓
Backend Creates Order
         ↓
Check Products for Webhooks
         ↓
Collect All Webhook URLs
         ↓
Build Discord Embed
         ↓
Send to All Webhooks (async)
         ↓
Log Success/Failure
         ↓
Continue Normal Order Flow
```

**Non-Blocking:**
- Webhook sending doesn't delay order creation
- Failures logged but don't break order flow
- Multiple webhooks sent in parallel

---

## 🧪 Testing

### Manual Test

1. **Create Test Webhook:**
   - Use Discord webhook tester or your own server
   
2. **Add to Product:**
   - Edit any product
   - Add webhook URL
   - Save

3. **Place Order:**
   - Go to product page
   - Complete order
   - Submit

4. **Check Discord:**
   - Should receive notification within seconds
   - Check embed formatting
   - Verify all order details

### Validation Checklist

- ✅ @everyone mention appears
- ✅ Embed displays correctly
- ✅ Order details accurate
- ✅ Customer info correct
- ✅ Total amount matches
- ✅ Product thumbnail shows
- ✅ Timestamp is current
- ✅ Color matches status

---

## 🐛 Troubleshooting

### Webhook Not Sending

**Check:**
1. ✅ Webhook URL is valid Discord webhook
2. ✅ Product has webhooks configured
3. ✅ Order was actually created (check admin panel)
4. ✅ Backend logs for errors: `tail -f /var/log/supervisor/backend.err.log`

**Common Issues:**
- Invalid webhook URL format
- Webhook deleted in Discord
- Discord server unavailable
- Network timeout

### Webhook URL Validation

**Valid:**
```
https://discord.com/api/webhooks/123456789/abcdefghijklmnop
https://ptb.discord.com/api/webhooks/123456789/abcdefghijklmnop
https://canary.discord.com/api/webhooks/123456789/abcdefghijklmnop
```

**Invalid:**
```
https://discord.gg/invite-code (This is invite link, not webhook)
discord.com/webhooks/... (Missing https://)
Not a URL at all
```

### Discord Rate Limits

**Limits:**
- 30 requests per 60 seconds per webhook
- If exceeded, webhook returns 429 error

**Solution:**
- Use multiple webhooks for high-volume products
- Backend automatically handles failures gracefully

---

## 📁 Technical Implementation

### Files Modified

**Backend:**
- `/app/backend/server.py`
  - Added `discord_webhooks` to Product models
  - Import discord_service
  - Remove webhooks from public API responses
  - Trigger webhook on order creation

**New Files:**
- `/app/backend/discord_service.py`
  - `send_discord_order_notification()` function
  - `send_discord_order_status_update()` function
  - Embed builder
  - HTTP client for Discord API

**Frontend:**
- `/app/frontend/src/pages/admin/AdminProducts.jsx`
  - Discord webhook UI section
  - Add/remove webhook functionality
  - Webhook list display

### Database Schema

```json
{
  "id": "product-uuid",
  "name": "Netflix Premium",
  "description": "...",
  "variations": [...],
  "discord_webhooks": [
    "https://discord.com/api/webhooks/123456789/abcdefghijklmnop",
    "https://discord.com/api/webhooks/987654321/zyxwvutsrqponmlk"
  ]
}
```

### API Endpoints

**Admin Only (webhooks included):**
- `POST /api/products` - Create with webhooks
- `PUT /api/products/{id}` - Update with webhooks

**Public (webhooks hidden):**
- `GET /api/products` - List products (no webhooks)
- `GET /api/products/{id}` - Get product (no webhooks)

---

## 🎯 Benefits

### For Business:
- ✅ Real-time order alerts
- ✅ Team collaboration in Discord
- ✅ No need to check admin panel constantly
- ✅ Mobile notifications via Discord app
- ✅ Historical order log in channels
- ✅ @everyone ensures no missed orders

### For Team:
- ✅ Instant awareness of new orders
- ✅ Quick response time
- ✅ Easy to discuss orders in thread
- ✅ Organized by channels/products
- ✅ Beautiful formatted messages

---

## 🚀 Advanced Features

### Multiple Webhooks Per Product

**Why?**
- Different teams need alerts
- Redundancy if one webhook fails
- Route to multiple channels

**Example:**
```
Product: High-Value Gaming PC
Webhooks:
  1. #sales-team (for processing)
  2. #management (for approval)
  3. #inventory (for stock tracking)
```

### Webhook Management

**Add Webhook:**
1. Paste URL
2. Click + button
3. Appears in list

**Remove Webhook:**
1. Click X button on webhook
2. Instantly removed

**Edit Webhook:**
1. Remove old webhook
2. Add new webhook

---

## 📝 Best Practices

1. **Use Dedicated Channels**
   - Create specific channels for order notifications
   - Don't spam general chat

2. **Test First**
   - Test with one webhook before adding multiple
   - Verify formatting and mentions work

3. **Organize by Product Type**
   - Gaming products → #gaming-orders
   - Streaming → #streaming-orders
   - Gift cards → #giftcard-orders

4. **Backup Webhooks**
   - Add 2+ webhooks for important products
   - Ensures notification delivery

5. **Monitor Logs**
   - Check backend logs occasionally
   - Verify webhooks are sending successfully

---

## 🆘 Support

### Get Help

**Backend Logs:**
```bash
tail -f /var/log/supervisor/backend.err.log | grep -i discord
```

**Test Webhook Manually:**
```bash
curl -X POST "https://discord.com/api/webhooks/YOUR_WEBHOOK" \
  -H "Content-Type: application/json" \
  -d '{"content": "Test message"}'
```

**Check Product Webhooks:**
```bash
# Login to MongoDB
mongo gameshop_nepal

# Find product
db.products.findOne({name: "Netflix Premium"}, {discord_webhooks: 1})
```

---

## ✅ Summary

**What Changed:**
1. ✅ Products can have Discord webhook URLs
2. ✅ Admin can add/remove multiple webhooks
3. ✅ Orders trigger automatic Discord notifications
4. ✅ Webhooks hidden from public API
5. ✅ Rich embeds with @everyone mentions
6. ✅ Beautiful formatted messages
7. ✅ Non-blocking async delivery

**Perfect For:**
- Real-time order tracking
- Team collaboration
- Mobile notifications
- Order history in Discord
- Customer service efficiency

---

Last Updated: February 18, 2026
