from django.core.management.base import BaseCommand
from itreporting.models import Module

class Command(BaseCommand):
    help = 'Adds default modules to the database'

    def handle(self, *args, **options):
        modules_data = [
            # Core modules
            {
                'name': 'Online Marketing',
                'code': 'CORE001',
                'credit': 20,
                'category': 'Core',
                'description': 'Learn the fundamentals of online marketing, including SEO, social media marketing, and digital advertising strategies.',
                'availability': 'open'
            },
            {
                'name': 'Online Coding',
                'code': 'CORE002',
                'credit': 20,
                'category': 'Core',
                'description': 'Introduction to programming concepts, web development, and software engineering principles.',
                'availability': 'open'
            },
            {
                'name': 'Online AI Learning',
                'code': 'CORE003',
                'credit': 20,
                'category': 'Core',
                'description': 'Explore artificial intelligence, machine learning, and their applications in modern technology.',
                'availability': 'open'
            },
            # Optional modules
            {
                'name': 'Video Editing',
                'code': 'OPT001',
                'credit': 15,
                'category': 'Optional',
                'description': 'Master video editing techniques, post-production workflows, and creative storytelling through video.',
                'availability': 'open'
            },
            {
                'name': 'Photoshop',
                'code': 'OPT002',
                'credit': 15,
                'category': 'Optional',
                'description': 'Learn professional image editing, graphic design, and digital art creation using Adobe Photoshop.',
                'availability': 'open'
            },
            # Elective modules
            {
                'name': 'Leadership Class',
                'code': 'ELE001',
                'credit': 10,
                'category': 'Elective',
                'description': 'Develop leadership skills, team management, and strategic thinking for professional growth.',
                'availability': 'open'
            },
            {
                'name': 'Team-Building Class',
                'code': 'ELE002',
                'credit': 10,
                'category': 'Elective',
                'description': 'Enhance collaboration, communication, and teamwork skills through interactive exercises and activities.',
                'availability': 'open'
            },
            # Foundation modules
            {
                'name': 'Starter Class',
                'code': 'FOU001',
                'credit': 10,
                'category': 'Foundation',
                'description': 'Essential skills for new students: time management, study techniques, and online learning best practices.',
                'availability': 'open'
            },
        ]
        
        created_count = 0
        skipped_count = 0
        
        for module_data in modules_data:
            module, created = Module.objects.get_or_create(
                code=module_data['code'],
                defaults={
                    'name': module_data['name'],
                    'credit': module_data['credit'],
                    'category': module_data['category'],
                    'description': module_data['description'],
                    'availability': module_data['availability']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created module: {module.code} - {module.name}')
                )
            else:
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Module already exists: {module.code} - {module.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Created {created_count} modules, skipped {skipped_count} existing modules.'
            )
        )

