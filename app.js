// Main App Script for Amazing UAE Store
class StoreApp {
    constructor() {
        this.cart = this.loadCart();
        this.products = [];
        this.currentPage = 1;
        this.productsPerPage = 12;
        this.init();
    }

    init() {
        this.loadProducts();
        this.setupEventListeners();
        this.updateCartBadge();
    }

    loadCart() {
        try {
            return JSON.parse(localStorage.getItem('amazing_uae_cart') || '[]');
        } catch {
            return [];
        }
    }

    saveCart() {
        localStorage.setItem('amazing_uae_cart', JSON.stringify(this.cart));
        this.updateCartBadge();
    }

    async loadProducts() {
        try {
            const response = await fetch('products-data.json');
            this.products = await response.json();
            this.renderProducts();
        } catch (error) {
            console.error('Error loading products:', error);
            this.showError();
        }
    }

    setupEventListeners() {
        const searchBox = document.getElementById('searchBox');
        const categoryFilter = document.getElementById('categoryFilter');
        const cartButton = document.getElementById('cartButton');

        if (searchBox) {
            searchBox.addEventListener('input', () => this.filterProducts());
        }

        if (categoryFilter) {
            categoryFilter.addEventListener('change', () => this.filterProducts());
        }

        if (cartButton) {
            cartButton.addEventListener('click', () => this.toggleCartDrawer());
        }
    }

    createSlug(title, id) {
        // إنشاء slug من العنوان
        let slug = title.toLowerCase()
            .replace(/[^\w\s-]/g, '')
            .replace(/\s+/g, '-')
            .replace(/-+/g, '-')
            .substring(0, 80);
        return `${slug}-${id}`;
    }

    filterProducts() {
        const searchTerm = document.getElementById('searchBox')?.value.toLowerCase() || '';
        const category = document.getElementById('categoryFilter')?.value || '';

        this.filteredProducts = this.products.filter(product => {
            const matchesSearch = product.title.toLowerCase().includes(searchTerm);
            const matchesCategory = !category || product.category === category;
            return matchesSearch && matchesCategory;
        });

        this.currentPage = 1;
        this.renderProducts();
    }

    renderProducts() {
        const grid = document.getElementById('productsGrid');
        if (!grid) return;

        const productsToShow = this.filteredProducts || this.products;
        const startIndex = (this.currentPage - 1) * this.productsPerPage;
        const endIndex = startIndex + this.productsPerPage;
        const pageProducts = productsToShow.slice(startIndex, endIndex);

        if (pageProducts.length === 0) {
            grid.innerHTML = '<div class="no-results">❌ لم يتم العثور على منتجات</div>';
            return;
        }

        grid.innerHTML = pageProducts.map(product => {
            const slug = product.slug || this.createSlug(product.title, product.id);
            const productUrl = `products/${slug}.html`;

            return `
            <div class="product-card" onclick="window.open('${productUrl}', '_blank')" style="cursor: pointer;">
                <img src="${product.image_link}" alt="${product.title}" class="product-image" loading="lazy">
                <div class="product-info">
                    <h3 class="product-title">${product.title}</h3>
                    <div class="product-price">${product.price} درهم</div>
                    <div class="product-actions">
                        <button onclick="event.stopPropagation(); window.storeApp.addToCart(${product.id})" class="btn btn-primary">
                            🛒 أضف للسلة
                        </button>
                        <button onclick="event.stopPropagation(); window.open('${productUrl}', '_blank')" class="btn btn-secondary">
                            👁️ التفاصيل
                        </button>
                    </div>
                </div>
            </div>
        `;
        }).join('');

        this.renderPagination(productsToShow.length);
    }

    renderPagination(totalProducts) {
        const pagination = document.getElementById('pagination');
        if (!pagination) return;

        const totalPages = Math.ceil(totalProducts / this.productsPerPage);
        if (totalPages <= 1) {
            pagination.innerHTML = '';
            return;
        }

        let paginationHTML = '<div class="pagination-controls">';

        if (this.currentPage > 1) {
            paginationHTML += `<button onclick="window.storeApp.goToPage(${this.currentPage - 1})" class="btn btn-outline">← السابق</button>`;
        }

        paginationHTML += `<span class="page-info">صفحة ${this.currentPage} من ${totalPages}</span>`;

        if (this.currentPage < totalPages) {
            paginationHTML += `<button onclick="window.storeApp.goToPage(${this.currentPage + 1})" class="btn btn-outline">التالي →</button>`;
        }

        paginationHTML += '</div>';
        pagination.innerHTML = paginationHTML;
    }

    goToPage(page) {
        this.currentPage = page;
        this.renderProducts();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    addToCart(productId) {
        const product = this.products.find(p => p.id == productId);
        if (!product) return;

        const existingItem = this.cart.find(item => item.id == productId);

        if (existingItem) {
            existingItem.quantity++;
        } else {
            this.cart.push({
                id: product.id,
                title: product.title,
                price: product.price,
                image: product.image_link,
                link: product.affiliate_link,
                quantity: 1
            });
        }

        this.saveCart();
        this.showAddedToCartMessage();
        this.toggleCartDrawer();
    }

    showAddedToCartMessage() {
        const message = document.createElement('div');
        message.style.cssText = 'position: fixed; top: 20px; right: 20px; background: #28a745; color: white; padding: 1rem 2rem; border-radius: 8px; z-index: 10001; animation: slideIn 0.3s;';
        message.innerHTML = '✅ تم إضافة المنتج للسلة';
        document.body.appendChild(message);
        setTimeout(() => message.remove(), 2000);
    }

    updateCartBadge() {
        const badge = document.getElementById('cartBadge');
        if (!badge) return;

        const totalItems = this.cart.reduce((sum, item) => sum + item.quantity, 0);

        if (totalItems > 0) {
            badge.textContent = totalItems;
            badge.style.display = 'flex';
        } else {
            badge.style.display = 'none';
        }
    }

    toggleCartDrawer() {
        const drawer = document.getElementById('cartDrawer');
        const overlay = document.getElementById('cartOverlay');

        if (!drawer || !overlay) return;

        const isOpen = drawer.style.right === '0px';

        if (isOpen) {
            drawer.style.right = '-100%';
            overlay.style.display = 'none';
        } else {
            drawer.style.right = '0';
            overlay.style.display = 'block';
            this.renderCartDrawer();
        }
    }

    renderCartDrawer() {
        const cartItems = document.getElementById('cartItems');
        const cartTotal = document.getElementById('cartTotal');

        if (!cartItems || !cartTotal) return;

        if (this.cart.length === 0) {
            cartItems.innerHTML = '<div style="text-align: center; padding: 2rem; color: #666;">🛒 السلة فارغة</div>';
            cartTotal.textContent = '0 درهم';
            return;
        }

        const total = this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        cartTotal.textContent = `${total.toFixed(2)} درهم`;

        cartItems.innerHTML = this.cart.map(item => `
            <div style="display: flex; gap: 1rem; padding: 1rem; border-bottom: 1px solid #eee;">
                <img src="${item.image}" alt="${item.title}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px;">
                <div style="flex: 1;">
                    <div style="font-weight: 600; margin-bottom: 0.5rem; font-size: 0.9rem;">${item.title.substring(0, 50)}...</div>
                    <div style="color: #FF9900; font-weight: 700;">${item.price} درهم × ${item.quantity}</div>
                    <div style="display: flex; gap: 0.5rem; margin-top: 0.5rem;">
                        <button onclick="window.storeApp.updateCartItem(${item.id}, ${item.quantity - 1})" style="padding: 0.25rem 0.5rem; background: #232F3E; color: white; border: none; border-radius: 4px; cursor: pointer;">−</button>
                        <span style="padding: 0.25rem 0.5rem;">${item.quantity}</span>
                        <button onclick="window.storeApp.updateCartItem(${item.id}, ${item.quantity + 1})" style="padding: 0.25rem 0.5rem; background: #232F3E; color: white; border: none; border-radius: 4px; cursor: pointer;">+</button>
                        <button onclick="window.storeApp.removeFromCart(${item.id})" style="padding: 0.25rem 0.5rem; background: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer; margin-left: auto;">🗑️</button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    updateCartItem(productId, newQuantity) {
        if (newQuantity <= 0) {
            this.removeFromCart(productId);
            return;
        }

        const item = this.cart.find(item => item.id == productId);
        if (item) {
            item.quantity = newQuantity;
            this.saveCart();
            this.renderCartDrawer();
        }
    }

    removeFromCart(productId) {
        this.cart = this.cart.filter(item => item.id != productId);
        this.saveCart();
        this.renderCartDrawer();
    }

    gotoCartPage() {
        window.location.href = 'cart.html';
    }

    buyAmazonNow() {
        if (this.cart.length === 0) {
            alert('السلة فارغة!');
            return;
        }
        window.open(this.cart[0].link, '_blank');
    }

    showError() {
        const grid = document.getElementById('productsGrid');
        if (grid) {
            grid.innerHTML = '<div class="error">❌ حدث خطأ في تحميل المنتجات</div>';
        }
    }
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.storeApp = new StoreApp();
    });
} else {
    window.storeApp = new StoreApp();
}

