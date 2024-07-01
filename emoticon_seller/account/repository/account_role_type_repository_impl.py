from account.entity.account_role_type import AccountRoleType
from account.repository.account_role_type_repository import AccountRoleTypeRepository


class AccountRoleTypeRepositoryImpl(AccountRoleTypeRepository):
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

    def findRoleTypeById(self, roleTypeId):
        try:
            accountRoleType = AccountRoleType.objects.get(id=roleTypeId)
            roleType = accountRoleType.roleType
            return roleType
        except AccountRoleType.DoesNotExist:
            print(f"id로 roleType을 찾을 수 없습니다.: {roleTypeId}")
            return None
        except Exception as e:
            print(f"roleType 찾는 중 에러 발생: {e}")
            return None
