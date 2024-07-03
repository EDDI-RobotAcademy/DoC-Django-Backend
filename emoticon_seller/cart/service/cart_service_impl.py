from account.repository.account_repository_impl import AccountRepositoryImpl
from cart.repository.cart_item_repository_impl import CartItemRepositoryImpl
from cart.repository.cart_repository_impl import CartRepositoryImpl
from cart.service.cart_service import CartService
from product.repository.product_repository_impl import ProductRepositoryImpl


class CartServiceImpl(CartService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cartRepository = CartRepositoryImpl.getInstance()
            cls.__instance.__productRepository = ProductRepositoryImpl.getInstance()
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()
            cls.__instance.__cartItemRepository = CartItemRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def cartRegister(self, cartData, accountId):
        account = self.__accountRepository.findById(accountId)
        cart = self.__cartRepository.findByAccount(account)
        if cart is None:
            print("장바구니 새롭게 생성")
            cart = self.__cartRepository.register(account)

        print("기존 장바구니 사용")

        productId = cartData.get('productId')
        cartItemList = self.__cartItemRepository.findAllByProductId(productId)

        cartItem = None
        for item in cartItemList:
            cartFromCartItem = item.cart
            accountFromCart = cartFromCartItem.account
            if accountFromCart.id == account.id:
                cartItem = item
                break
        if cartItem is None:
            print("신규 상품 추가")
            product = self.__productRepository.findByProductId(productId)
            self.__cartItemRepository.register(cartData, cart, product)

    def cartList(self, accountId):
        account = self.__accountRepository.findById(accountId)
        cart = self.__cartRepository.findByAccount(account)
        # print(f"cartList -> cart: {cart}")
        cartItemList = self.__cartItemRepository.findByCart(cart)
        # print(f"cartList -> cartItemList: {cartItemList}")

        cartItemListResponseForm = []

        for cartItem in cartItemList:
            cartItemResponseForm = {
                'cartItemId': cartItem.cartItemId,
                'productName': cartItem.product.productName,
                'productPrice': cartItem.product.productPrice,
                'productTitleImage': cartItem.product.productTitleImage,
                'productId': cartItem.product.productId,
                'quantity': cartItem.quantity,
            }
            cartItemListResponseForm.append(cartItemResponseForm)

        return cartItemListResponseForm

    def removeCartItem(self, cartItemId):
        self.__cartItemRepository.deleteByCartItemId(cartItemId)




