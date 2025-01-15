from django.core.management.base import BaseCommand
from django.conf import settings
from main.models import * 

class Command(BaseCommand):
    help = 'Cria o pefil do bot'

    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            type=str,
            help='Cria o bot com um nome personalizado'
        )

    def handle(self, *args, **options):
        name = options.get('name')

        name = name if name else "bot"

            
        self.stdout.write(self.style.WARNING(f'O bot sera criado com o nome de: {self.style.SUCCESS(name)}'))
            
        try:
            self.stdout.write("Criando bot...")
            perfil, created =  Profile.objects.get_or_create(wa_id=settings.NUMBER_ID)

            if created:
                perfil.name = name
                perfil.save()
                self.stdout.write(self.style.SUCCESS('Bot criado com sucesso...'))
            else:
                self.stdout.write(self.style.NOTICE(f'O bot já existe com o nome de: {perfil.name}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao criar bot: {e}'))