from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Product, Business

products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
@login_required
def list_products():
    """Lista todos os produtos do usuário"""
    # Buscar negócio do usuário
    business = Business.query.filter_by(user_id=current_user.id).first()
    
    if not business:
        flash('Você precisa ter um negócio cadastrado para gerenciar produtos.', 'warning')
        return redirect(url_for('business.edit_business'))
    
    products = Product.query.filter_by(business_id=business.id).all()
    return render_template('products/list.html', products=products, business=business)

@products_bp.route('/products/new', methods=['GET', 'POST'])
@login_required
def create_product():
    """Criar novo produto"""
    business = Business.query.filter_by(user_id=current_user.id).first()
    
    if not business:
        flash('Você precisa ter um negócio cadastrado para adicionar produtos.', 'warning')
        return redirect(url_for('business.edit_business'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        category = request.form.get('category')
        tags = request.form.get('tags')
        
        product = Product(
            name=name,
            description=description,
            price=float(price) if price else None,
            category=category,
            tags=tags,
            business_id=business.id
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('products.list_products'))
    
    return render_template('products/form.html', business=business)

@products_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    """Editar produto existente"""
    product = Product.query.get_or_404(product_id)
    business = Business.query.filter_by(user_id=current_user.id).first()
    
    # Verificar se o produto pertence ao usuário
    if product.business_id != business.id:
        flash('Acesso não autorizado.', 'error')
        return redirect(url_for('products.list_products'))
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price')) if request.form.get('price') else None
        product.category = request.form.get('category')
        product.tags = request.form.get('tags')
        
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('products.list_products'))
    
    return render_template('products/form.html', product=product, business=business)

@products_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    """Deletar produto"""
    product = Product.query.get_or_404(product_id)
    business = Business.query.filter_by(user_id=current_user.id).first()
    
    if product.business_id != business.id:
        flash('Acesso não autorizado.', 'error')
        return redirect(url_for('products.list_products'))
    
    db.session.delete(product)
    db.session.commit()
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('products.list_products'))

@products_bp.route('/api/products')
@login_required
def api_products():
    """API para listar produtos (usado no swipe)"""
    business_id = request.args.get('business_id')
    
    if business_id:
        products = Product.query.filter_by(business_id=business_id, active=True).all()
    else:
        # Listar produtos de outros negócios (para swipe)
        user_business = Business.query.filter_by(user_id=current_user.id).first()
        if user_business:
            products = Product.query.filter(
                Product.business_id != user_business.id,
                Product.active == True
            ).all()
        else:
            products = []
    
    return jsonify([product.to_dict() for product in products])
