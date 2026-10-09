from django.core.management.base import BaseCommand
from django.utils import timezone

from agent_api.models import AgentApiKey


class Command(BaseCommand):
    help = "Manage machine-to-machine YojanaSaathi Agent API keys (create, list, revoke, rotate)"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="action", required=True)

        # Create
        create_p = subparsers.add_parser("create", help="Create a new Agent API key")
        create_p.add_argument("--name", default="YojanaSaathi AI Agent", help="Descriptive name")

        # List
        subparsers.add_parser("list", help="List all Agent API keys")

        # Revoke
        revoke_p = subparsers.add_parser("revoke", help="Revoke an existing key")
        revoke_p.add_argument("--prefix", required=True, help="Prefix of the key to revoke")

        # Rotate
        rotate_p = subparsers.add_parser("rotate", help="Create a replacement key and revoke the old one")
        rotate_p.add_argument("--old-prefix", required=True, help="Prefix of the old key")
        rotate_p.add_argument("--name", default="Rotated YojanaSaathi AI Agent", help="Name for new key")

    def handle(self, *args, **options):
        action = options["action"]

        if action == "create":
            name = options["name"]
            key_obj, raw_secret = AgentApiKey.create_key(name=name)
            self.stdout.write(self.style.SUCCESS("\n=== AGENT API KEY CREATED SUCCESSFULLY ==="))
            self.stdout.write(f"Name:       {key_obj.name}")
            self.stdout.write(f"Prefix:     {key_obj.key_prefix}")
            self.stdout.write(f"Created At: {key_obj.created_at}")
            self.stdout.write(self.style.WARNING("\n[IMPORTANT] Secret API Key (Displaying ONCE, cannot be retrieved again):"))
            self.stdout.write(self.style.SUCCESS(f"{raw_secret}\n"))
            self.stdout.write("Configure this in your external AI agent environment as:")
            self.stdout.write(f"YOJANASAATHI_AGENT_API_KEY={raw_secret}\n")

        elif action == "list":
            keys = AgentApiKey.objects.all().order_by("-created_at")
            if not keys.exists():
                self.stdout.write("No Agent API keys found.")
                return

            self.stdout.write("\n{:<36} {:<16} {:<10} {:<24} {:<24}".format(
                "Name", "Prefix", "Status", "Created At", "Last Used"
            ))
            self.stdout.write("-" * 115)
            for k in keys:
                status_str = "ACTIVE" if k.is_active else "REVOKED"
                last_used = k.last_used_at.strftime("%Y-%m-%d %H:%M:%S") if k.last_used_at else "Never"
                created = k.created_at.strftime("%Y-%m-%d %H:%M:%S")
                self.stdout.write("{:<36} {:<16} {:<10} {:<24} {:<24}".format(
                    k.name[:35], k.key_prefix, status_str, created, last_used
                ))

        elif action == "revoke":
            prefix = options["prefix"]
            key_obj = AgentApiKey.objects.filter(key_prefix__startswith=prefix).first()
            if not key_obj:
                self.stdout.write(self.style.ERROR(f"No key found matching prefix '{prefix}'."))
                return

            if not key_obj.is_active:
                self.stdout.write(self.style.WARNING(f"Key '{key_obj.name}' ({key_obj.key_prefix}) is already revoked."))
                return

            key_obj.revoke()
            self.stdout.write(self.style.SUCCESS(f"Successfully revoked key '{key_obj.name}' ({key_obj.key_prefix})."))

        elif action == "rotate":
            old_prefix = options["old_prefix"]
            old_key = AgentApiKey.objects.filter(key_prefix__startswith=old_prefix, is_active=True).first()
            if not old_key:
                self.stdout.write(self.style.ERROR(f"Active key with prefix '{old_prefix}' not found."))
                return

            name = options["name"]
            new_key, raw_secret = AgentApiKey.create_key(name=name)
            old_key.revoke()

            self.stdout.write(self.style.SUCCESS("\n=== AGENT API KEY ROTATED ==="))
            self.stdout.write(f"Revoked old key: {old_key.name} ({old_key.key_prefix})")
            self.stdout.write(f"Created new key: {new_key.name} ({new_key.key_prefix})")
            self.stdout.write(self.style.WARNING("\nNew Secret API Key:"))
            self.stdout.write(self.style.SUCCESS(f"{raw_secret}\n"))
