"""
Discord Webhook Service
Sends order notifications to Discord via webhooks
"""
import httpx
import logging
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)


async def send_discord_order_notification(
    webhook_urls: List[str],
    order_data: dict,
    product_data: dict = None
):
    """
    Send order notification to Discord webhooks
    
    Args:
        webhook_urls: List of Discord webhook URLs
        order_data: Order information
        product_data: Product information (optional)
    """
    if not webhook_urls:
        return
    
    # Prepare embed data
    order_id = order_data.get('id', 'N/A')
    customer_name = order_data.get('customer_name', 'N/A')
    customer_email = order_data.get('customer_email', 'N/A')
    customer_phone = order_data.get('customer_phone', 'N/A')
    total_amount = order_data.get('total_amount', 0)
    items = order_data.get('items', [])
    status = order_data.get('status', 'pending')
    remark = order_data.get('remark', '')
    
    # Build items description
    items_description = ""
    for item in items:
        quantity = item.get('quantity', 1)
        name = item.get('name', 'Unknown')
        variation = item.get('variation', '')
        price = item.get('price', 0)
        
        variation_text = f" ({variation})" if variation else ""
        items_description += f"• **{quantity}x** {name}{variation_text} - Rs {price:,.2f}\n"
    
    # Status emoji
    status_emojis = {
        'pending': '⏳',
        'processing': '🔄',
        'completed': '✅',
        'cancelled': '❌'
    }
    status_emoji = status_emojis.get(status, '📦')
    
    # Status colors
    status_colors = {
        'pending': 0xFFA500,      # Orange
        'processing': 0x3498DB,   # Blue
        'completed': 0x2ECC71,    # Green
        'cancelled': 0xE74C3C     # Red
    }
    color = status_colors.get(status, 0x95A5A6)  # Gray default
    
    # Build Discord embed
    embed = {
        "content": "@everyone 🔔 **New Order Received!**",
        "embeds": [{
            "title": f"{status_emoji} New Order - #{order_id[:8].upper()}",
            "description": f"A new order has been placed on GameShop Nepal!",
            "color": color,
            "fields": [
                {
                    "name": "👤 Customer Name",
                    "value": customer_name,
                    "inline": True
                },
                {
                    "name": "📧 Email",
                    "value": customer_email,
                    "inline": True
                },
                {
                    "name": "📱 Phone",
                    "value": customer_phone,
                    "inline": True
                },
                {
                    "name": "📦 Order Items",
                    "value": items_description if items_description else "No items",
                    "inline": False
                },
                {
                    "name": "💰 Total Amount",
                    "value": f"**Rs {total_amount:,.2f}**",
                    "inline": True
                },
                {
                    "name": "📊 Status",
                    "value": f"{status_emoji} {status.upper()}",
                    "inline": True
                },
                {
                    "name": "🆔 Order ID",
                    "value": f"`{order_id}`",
                    "inline": True
                }
            ],
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                "text": "GameShop Nepal - Order Management",
                "icon_url": "https://customer-assets.emergentagent.com/job_8ec93a6a-4f80-4dde-b760-4bc71482fa44/artifacts/4uqt5osn_Staff.zip%20-%201.png"
            }
        }]
    }
    
    # Add remark field if exists
    if remark and remark.strip():
        embed["embeds"][0]["fields"].append({
            "name": "📝 Remarks",
            "value": remark[:1024],  # Discord limit
            "inline": False
        })
    
    # Add product info if provided
    if product_data:
        product_name = product_data.get('name', 'N/A')
        product_image = product_data.get('image_url')
        
        if product_image:
            embed["embeds"][0]["thumbnail"] = {"url": product_image}
        
        embed["embeds"][0]["author"] = {
            "name": f"Product: {product_name}",
            "icon_url": "https://cdn-icons-png.flaticon.com/512/869/869636.png"
        }
    
    # Send to all webhooks
    async with httpx.AsyncClient(timeout=10.0) as client:
        for webhook_url in webhook_urls:
            if not webhook_url or not webhook_url.strip():
                continue
            
            try:
                response = await client.post(webhook_url, json=embed)
                
                if response.status_code in [200, 204]:
                    logger.info(f"✅ Discord webhook sent successfully to {webhook_url[:50]}...")
                else:
                    logger.error(f"❌ Discord webhook failed: {response.status_code} - {response.text}")
            
            except Exception as e:
                logger.error(f"❌ Failed to send Discord webhook: {str(e)}")


async def send_discord_order_status_update(
    webhook_urls: List[str],
    order_data: dict,
    old_status: str,
    new_status: str
):
    """
    Send order status update to Discord webhooks
    
    Args:
        webhook_urls: List of Discord webhook URLs
        order_data: Order information
        old_status: Previous status
        new_status: New status
    """
    if not webhook_urls:
        return
    
    order_id = order_data.get('id', 'N/A')
    customer_name = order_data.get('customer_name', 'N/A')
    total_amount = order_data.get('total_amount', 0)
    
    # Status emojis
    status_emojis = {
        'pending': '⏳',
        'processing': '🔄',
        'completed': '✅',
        'cancelled': '❌'
    }
    
    # Status colors
    status_colors = {
        'pending': 0xFFA500,
        'processing': 0x3498DB,
        'completed': 0x2ECC71,
        'cancelled': 0xE74C3C
    }
    color = status_colors.get(new_status, 0x95A5A6)
    
    old_emoji = status_emojis.get(old_status, '📦')
    new_emoji = status_emojis.get(new_status, '📦')
    
    # Build Discord embed
    embed = {
        "content": f"@everyone 📢 **Order Status Updated!**",
        "embeds": [{
            "title": f"{new_emoji} Order Status Changed - #{order_id[:8].upper()}",
            "description": f"Status: {old_emoji} **{old_status.upper()}** → {new_emoji} **{new_status.upper()}**",
            "color": color,
            "fields": [
                {
                    "name": "👤 Customer",
                    "value": customer_name,
                    "inline": True
                },
                {
                    "name": "💰 Amount",
                    "value": f"Rs {total_amount:,.2f}",
                    "inline": True
                },
                {
                    "name": "🆔 Order ID",
                    "value": f"`{order_id}`",
                    "inline": True
                }
            ],
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                "text": "GameShop Nepal - Order Management"
            }
        }]
    }
    
    # Send to all webhooks
    async with httpx.AsyncClient(timeout=10.0) as client:
        for webhook_url in webhook_urls:
            if not webhook_url or not webhook_url.strip():
                continue
            
            try:
                response = await client.post(webhook_url, json=embed)
                
                if response.status_code in [200, 204]:
                    logger.info(f"✅ Discord status update sent to {webhook_url[:50]}...")
                else:
                    logger.error(f"❌ Discord webhook failed: {response.status_code}")
            
            except Exception as e:
                logger.error(f"❌ Failed to send Discord webhook: {str(e)}")
