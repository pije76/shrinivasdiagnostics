
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile']
        def create(self, validated_data):
            instance = self.Meta.model(**validated_data)
            global totp
            secret = pyotp.random_base32()
            totp = pyotp.TOTP(secret, interval=300)
            otp = totp.now()
            instance = self.Meta.model.objects.update_or_create(**validated_data, defaults=dict(otp=str(random.randint(1000 , 9999))))[0]
            instance.save()
            return instance

class VerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile','otp']

        def create(self,validated_data):
            instance = self.Meta.model(**validated_data)
            mywords = "123456789"
            res = "expert@" + str(''.join(random.choices(mywords,k = 6)))
            path = os.path.join(BASE_DIR, 'static')
            dir_list = os.listdir(path)
            random_logo = random.choice(dir_list)
            instance = self.Meta.model.objects.update_or_create(**validated_data, defaults = dict(username = res, full_name = instance.mobile ,logo = random_logo, profile_id = res))[0]
            instance.save()
        return instance
