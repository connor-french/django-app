from django.contrib.auth.models import User
from learner.models import Profile, ProfileLink
from django.core.management import BaseCommand
from django.core.files import File
from django.conf import settings
from backend.dhri.log import Logger, Input
from ._shared import test_for_required_files, get_yaml, LogSaver
import os


SAVE_DIR = f'{settings.BASE_DIR}/_preload/_meta/users'
FULL_PATH = f'{SAVE_DIR}/users.yml'
REQUIRED_PATHS = [
    (SAVE_DIR,
     f'The required directory ({SAVE_DIR}) does not exist. Did you run `python manage.py buildusers` before you ran this command?'),
    (FULL_PATH,
     f'The required data file ({FULL_PATH}) does not exist. Did you run `python manage.py buildusers` before you ran this command?')
]


def get_profile_picture_path(image_file, relative_to_upload_field=False):
    if not relative_to_upload_field:
        return settings.MEDIA_ROOT + '/' + Profile.image.field.upload_to + '/' + os.path.basename(image_file)

    return Profile.image.field.upload_to + '/' + os.path.basename(image_file)


def profile_picture_exists(image_file):
    return os.path.exists(get_profile_picture_path(image_file))


def get_default_profile_picture(full_path=False):
    if full_path == False:
        return Profile.image.field.upload_to + '/' + Profile.image.field.default
    return settings.MEDIA_ROOT + '/' + Profile.image.field.upload_to + \
        '/' + Profile.image.field.default


class Command(LogSaver, BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = 'Ingests internal DHRI YAML files with user information into the database'
    requires_migrations_checks = True
    SAVE_DIR = ''
    WARNINGS, LOGS = [], []

    def add_arguments(self, parser):
        parser.add_argument('--forceupdate', action='store_true')
        parser.add_argument('--silent', action='store_true')
        parser.add_argument('--verbose', action='store_true')

    def handle(self, *args, **options):
        log = Logger(path=__file__,
                     force_verbose=options.get('verbose'),
                     force_silent=options.get('silent')
                     )
        input = Input(path=__file__)

        test_for_required_files(REQUIRED_PATHS=REQUIRED_PATHS, log=log)
        data = get_yaml(f'{FULL_PATH}')

        for userdata in data.get('users', []):
            if not userdata.get('username'):
                log.error(
                    f'Username is required. Check the datafile ({FULL_PATH}) to make sure that all the users in the file are assigned a username.')

            finder = User.objects.filter(username=userdata.get('username'))
            if finder.count():
                finder.update(
                    first_name=userdata.get('first_name'),
                    last_name=userdata.get('last_name'),
                    email=userdata.get('email'),
                    is_staff=userdata.get('staff')
                )
                
                user = User.objects.get(username=userdata.get('username'))
            else:
                func = User.objects.create_user
                if userdata.get('superuser'):
                    func = User.objects.create_superuser

                user = func(
                    username=userdata.get('username'),
                    first_name=userdata.get('first_name'),
                    last_name=userdata.get('last_name'),
                    email=userdata.get('email'),
                    is_staff=userdata.get('staff')
                )

                user.refresh_from_db()

            # if None, sets to unusable password, see https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#django.contrib.auth.models.User.set_password
            user.set_password(userdata.get('password'))
            user.save()

            if not userdata.get('profile'):
                log.error(f'User {userdata.get("username")} does not have profile information (bio, image, links, and/or pronouns) added. Make sure you add all this information for each user in the datafile before running this command ({FULL_PATH}).')

            profile, created = Profile.objects.get_or_create(user=user)

            if not created and not options.get('forceupdate'):
                choice = input.ask(
                    f'User `{userdata.get("username")}` already has a profile. Update with new information? [y/N]')
                if choice.lower() != 'y':
                    continue

            Profile.objects.filter(user=user).update(
                bio=userdata.get('profile', {}).get('bio'),
                pronouns=userdata.get('profile', {}).get('pronouns'),
            )

            profile.refresh_from_db()

            if userdata.get('profile', {}).get('image'):
                if profile_picture_exists(userdata.get('profile', {}).get('image')):
                    profile.image.name = get_profile_picture_path(
                        userdata.get('profile', {}).get('image'), True)
                    profile.save()
                else:
                    with open(userdata.get('profile', {}).get('image'), 'rb') as f:
                        profile.image = File(f, name=os.path.basename(f.name))
                        profile.save()
            else:
                profile.image.name = get_default_profile_picture()
                profile.save()

            if userdata.get('profile', {}).get('links'):
                for link in userdata.get('profile', {}).get('links'):
                    if link.get('cat') == 'personal':
                        link['cat'] = ProfileLink.PERSONAL
                    elif link.get('cat') == 'project':
                        link['cat'] = ProfileLink.PROJECT
                    else:
                        log.error(
                            f'Link {link.get("url")} is assigned a category that has no correspondence in the database model: {link.get("cat")}. Please set the category to either `personal` or `project`.')

                    _, _ = ProfileLink.objects.get_or_create(profile=profile, url=link.get('url'), defaults={
                        'cat': link.get('cat'),
                        'label': link.get('label')
                    })

                    ProfileLink.objects.filter(profile=profile, url=link.get('url')).update(
                        cat=link.get('cat'),
                        label=link.get('label')
                    )

        if not profile_picture_exists(get_default_profile_picture(full_path=True)):
            if data.get('default', False) and os.path.exists(data.get('default')):
                from shutil import copyfile

                copyfile(data.get('default'),
                         get_default_profile_picture(full_path=True))
                self.LOGS.append(log.log(
                    'Default profile picture added to the /media/ directory.'))
            elif not data.get('default'):
                log.error(
                    f'No default profile picture was defined in your datafile (`{FULL_PATH}`). Add the file, and then add the path to the file (relative to the `django-app` directory) in a `default` dictionary in your `users.yml` file, like this:\n' + '`default: backend/setup/users/default.jpg`')
            elif not os.path.exists(data.get('default')):
                log.error(
                    f'The default profile picture (`{data.get("default")}`) in your datafile (`{FULL_PATH}`) does not exist in its expected directory (`{os.path.dirname(data.get("default"))}`). Make sure it is in the directory or update the datafile accordingly, or add the file before running this command.')

        self.LOGS.append(log.log('Added/updated users: ' +
                                 ', '.join([x.get('username') for x in data.get('users')])))

        self.SAVE_DIR = self.SAVE_DIR = f'{LogSaver.LOG_DIR}/ingestusers'
        if self._save(data='ingestusers', name='warnings.md', warnings=True) or self._save(data='ingestusers', name='logs.md', warnings=False, logs=True):
            log.log('Log files with any warnings and logging information is now available in the' +
                    self.SAVE_DIR, force=True)
