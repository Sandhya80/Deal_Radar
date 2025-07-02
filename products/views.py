"""
Product Views for Deal Radar - Phase 2
Simple product display functionality
"""

from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

def home(request):
    """Phase 2: Simple homepage showing products from Phase 1 admin"""
    try:
        # Get all products added via admin (Phase 1)
        products = Product.objects.all().order_by('-created_at')
        total_products = products.count()
        
        # Build a clean HTML page showing Phase 1 work
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Deal Radar - Phases 1 & 2</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 40px; 
                    background-color: #f5f5f5;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .stats {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .product {{ 
                    background: white;
                    border: 1px solid #ddd; 
                    padding: 20px; 
                    margin: 15px 0; 
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .product h3 {{ color: #333; margin-top: 0; }}
                .price {{ 
                    font-size: 24px; 
                    font-weight: bold; 
                    color: #e74c3c; 
                }}
                .meta {{ color: #666; font-size: 14px; }}
                .no-products {{ 
                    text-align: center; 
                    padding: 40px; 
                    background: white; 
                    border-radius: 8px; 
                }}
                .admin-link {{
                    display: inline-block;
                    background: #3498db;
                    color: white;
                    padding: 12px 24px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 10px 5px;
                }}
                .admin-link:hover {{ background: #2980b9; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎯 Deal Radar</h1>
                <p>Phase 1: Admin Interface ✅ | Phase 2: Product Display ✅</p>
            </div>
            
            <div class="stats">
                <h2>📊 Project Status</h2>
                <p><strong>Products in Database:</strong> {total_products}</p>
                <p><strong>Phase 1 Complete:</strong> ✅ Admin interface for product management</p>
                <p><strong>Phase 2 Complete:</strong> ✅ Public website displaying products</p>
                <p><strong>Next:</strong> Phase 3 will add user accounts and personal tracking</p>
            </div>
            
            <h2>🛍️ Products Being Tracked</h2>
        """
        
        if products:
            for product in products:
                # Format the price display
                price_display = f"£{product.current_price}" if product.current_price else "Price not set"
                
                # Format dates nicely
                created_date = product.created_at.strftime("%B %d, %Y at %I:%M %p")
                
                html += f"""
                <div class="product">
                    <h3>{product.name}</h3>
                    <div class="price">{price_display}</div>
                    <div class="meta">
                        <p><strong>Site:</strong> {product.site_name or 'Not specified'}</p>
                        <p><strong>Category:</strong> {product.category or 'Uncategorized'}</p>
                        <p><strong>Added:</strong> {created_date}</p>
                        <p><strong>Description:</strong> {product.description[:100] + '...' if len(product.description) > 100 else product.description}</p>
                        <p><a href="{product.url}" target="_blank" style="color: #3498db;">🔗 View on {product.site_name or 'Website'}</a></p>
                    </div>
                </div>
                """
        else:
            html += """
            <div class="no-products">
                <h3>No Products Yet</h3>
                <p>No products have been added to the database yet.</p>
                <p>Use the admin panel below to add your first products!</p>
            </div>
            """
        
        html += f"""
            <div style="text-align: center; margin-top: 40px; padding: 30px; background: white; border-radius: 8px;">
                <h3>🔧 Admin Controls (Phase 1)</h3>
                <p>Add, edit, and manage products using the Django admin interface:</p>
                <a href="/admin/" class="admin-link">🎛️ Admin Panel</a>
                <a href="/admin/products/product/add/" class="admin-link">➕ Add New Product</a>
                
                <hr style="margin: 30px 0;">
                
                <h3>🚀 Coming in Phase 3</h3>
                <p>• User accounts and authentication<br>
                • Personal product tracking lists<br>
                • Price alert notifications<br>
                • Individual user dashboards</p>
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(html)
        
    except Exception as e:
        # Error handling - show what went wrong
        return HttpResponse(f"""
        <h1>Deal Radar - Debug Mode</h1>
        <p><strong>Error:</strong> {str(e)}</p>
        <p><strong>Phase Status:</strong></p>
        <ul>
            <li>Phase 1: Admin setup - Should be working</li>
            <li>Phase 2: Product display - Currently debugging</li>
        </ul>
        <p><a href="/admin/">Try Admin Panel</a></p>
        """)
