from django_grpc_framework.management.commands.grpcrunserver import Command as GrpcRunserverCommand
import os

class Command(GrpcRunserverCommand):
    requires_system_checks = []
    # change port
    # set address here 
    address = os.environ.get('BASE_INFO_GRPC_ADDRESS', '[::]:50052')
    def handle(self, *args, **options):
        self.address = self.address
        self.development_mode = options['development_mode']
        self.max_workers = options['max_workers']
        self.run(**options)

   