from cart.entity.cart import Cart
from cart.entity.cart_item import CartItem
from cart.repository.cart_item_repository import CartItemRepository


class CartItemRepositoryImpl(CartItemRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def register(self, cartData, cart, product):
        productPrice = cartData.get('productPrice')

        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1,
            price=productPrice
        )

    def findByCart(self, cart):
        return list(CartItem.objects.filter(cart=cart))

    def findByProductId(self, productId):
        try:
            return CartItem.objects.get(product_id=productId)
        except CartItem.DoesNotExist:
            return None

    def findAllByProductId(self, productId):
        return CartItem.objects.filter(product_id=productId)

    def findById(self, id):
        return CartItem.objects.get(cartItemId=id)


    def deleteByCartItemId(self, cartItemIdList):
        for cartItemId in cartItemIdList:
            cartItem = CartItem.objects.get(cartItemId=cartItemId)
            cartItem.delete()

    def checkDuplication(self, cartItemList, productId):
        for cartItem in cartItemList:
            if cartItem.product.productId == productId:
                return True

        return False



