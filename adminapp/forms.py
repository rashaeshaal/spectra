from django import forms
from .models import Category
from .models import Products,ProductImage
#from .models import Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products  # Replace 'Products' with your model name
        fields = ['product_name', 'product_brand', 'product_category', 'product_price', 'quantity', 'product_details', 'product_image', 'offer_price', 'product_status']
        
        
        

class ProductGalleryForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product', 'image']

# class ProductImageForm(forms.Form):
#     images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ('product_name', 'description', 'price', 'quantity', 'product_category')

        

        
