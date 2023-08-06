# Quart-Keycloak

zZzZ

### Redis cache

```python3
app.setup_cache()
```

After which you may use it directly;

```python3
from quart_session.sessions import SessionInterface
@app.route("/")
async def hello():
    cache: SessionInterface = app.session_interface
    await cache.set("random_key", "val", expiry=3600)
    data = await cache.get("random_key")
```

### multi-subscriber websocket

```python3
from asyncio_multisubscriber_queue import MultisubscriberQueue
broadcast = MultisubscriberQueue()

await broadcast.put({"payload": 1})

async for msg in broadcast.subscribe():
    [...]
```

### Utils

```python3
from quart.kroket.utils import ...
```

```python3
def make_slug(inp: str)
def program_exists(name: str)
def safu(func)  (decorator)
def get_visitor_ipv4(enforce_forwarded_header=True)
def random_str(num_chars: int)
```

### image APIs

```text
app.setup_image_apis()
```

Registers the following routes:

- `/_/avatar/<path:inp>`
- `/_/gravatar/<path:inp>`
- `/_/avatar/<path:inp>`
- `/_/qr/<path:inp>/<path:color_from>/<path:color_to>/` (colors need to be tuple)

```python3
url_for("kquart.route_avatar", inp="test")
url_for("kquart.route_gravatar", inp="test")
url_for("kquart.route_qr", inp="test")
```

### Error templates

Create these:

- `templates/errors/500.html`
- `templates/errors/403.html`
- `templates/errors/404.html`

### OIDC

```python3
app.setup_keycloak(
    client_id='', 
    client_secret='', 
    configuration='url')
```

auto-registered routes:

- `/oidc/login`
- `/oidc/logout`
- `/oidc/after_logout`

After login, will set `g.user` and `session['user']` with instance of `quart.kroket.oidc.models.KeycloakUser`

So in `factory.py` we'll have `before_request` look like:

```python3
@app.before_request
async def set_request_ctx():
    from app.db.models import User
    from quart.kroket.database.enums import UserRole
    auth_token: KeycloakAuthToken = g.ses

    if not auth_token:
        return

    if g.user:
        return

    # get and update (or create) user
    try:
        user: User = User.by_uid(auth_token.sub)
        user.username = auth_token.username
        user.role = UserRole.member
        user.save()
        g.user = user
    except pw.DoesNotExist as ex:
        user: User = User.create(
            uuid=auth_token.sub,
            username=auth_token.username,
            role=UserRole.member)
        g.user = user
    except Exception as ex:
        current_app.logger.error(ex)
        session.clear()
        raise Exception(ex)
```

### Template filters

```text
hash_sha256(val)
def hash_md5(val)
def size_human(val)
def dt_ago(val: datetime)
def dt_human(val)
```

### Rate limiting

```python3
rate_limiter = RateLimiter()

def create_app():
    app = Quart(__name__)
    rate_limiter.init_app(app)
    return app

@app.route('/')
@rate_limit(1, timedelta(seconds=10))
async def handler():
    [...]
```

### Database
#### Enum

```text
Usage:
  from enum import IntEnum, unique

  @unique
  class UserStatus(IntEnum):
    disabled = 0
    enable = 1
    banned = 2

  [...]
  status = EnumIntField(enum_class=UserStatus, default=UserStatus.active)
  [...]
  Model.select().where(Model.status != UserStatus.banned)

Usage:
  from enum import IntEnum, unique

  @unique
  class UserTags(IntEnum):
    has_car = 0
    has_plane = 1
    has_helicopter = 2

  [...]
  vehicles = EnumArrayField(enum_class=UserTags, field_class=IntegerField, default=[UserTags.has_bank_account])

  # Fetch results with `has_car` OR `has_helicopter`:
  Model.select().where(
    Model.vehicles.contains_any(UserTags.has_car, UserTags.has_helicopter)).get()
```

#### database example

```python3
from quart.kroket.database import create_db
database = create_db()
```

```python3
class Company(pw.Model):
    uid: Union[str, UUID] = pw.UUIDField(primary_key=True, default=uuid4)
    created = pw.DateTimeField(default=datetime.now)
    modified = pw.DateTimeField(default=datetime.now)

    name: str = pw.CharField(unique=True, index=True, max_length=256)
    users: List['User'] = None

    class Meta:
        from my_app.factory import database
        database = database


class User(pw.Model):
    uid: Union[str, UUID] = pw.UUIDField(primary_key=True)  # uuid4 from keycloak
    created = pw.DateTimeField(default=datetime.now)
    modified = pw.DateTimeField(default=datetime.now)

    name = pw.CharField(unique=True, index=True, max_length=256)
    username = pw.CharField(unique=True, index=True, max_length=64)
    company = pw.ForeignKeyField(Company, backref='users')

    roles: List[UserRole] = EnumArrayField(enum_class=UserRole, field_class=pw.IntegerField, default=[UserRole.anonymous])
    status: UserStatus = EnumIntField(enum_class=UserStatus, default=UserStatus.active)

    things: List['Thing'] = None

    class Meta:
        from my_app.factory import database
        database = database

    @property
    def is_admin(self):
        return UserRole.admin in self.roles

    @property
    def is_anon(self):
        return UserRole.anonymous in self.roles

    @property
    def has_auth(self):
        return not self.is_anon

    @staticmethod
    def by_uid(uuid: Union[str, UUID]):
        return User.select() \
            .join(File, pw.JOIN.LEFT_OUTER) \
            .where(User.uid == uuid).get()
        # .join(Download, pw.JOIN.LEFT_OUTER) \

    async def to_json(self):
        return {
            "uid": self.uid
        }


class Thing(pw.Model):
    uid: Union[str, UUID] = pw.UUIDField(primary_key=True, default=uuid4)
    created = pw.DateTimeField(default=datetime.now)
    modified = pw.DateTimeField(default=datetime.now)

    title: str = pw.CharField(max_length=512, index=True)
    markdown: str = pw.TextField(null=True)

    roles_view: List[UserRole] = EnumArrayField(enum_class=UserRole, field_class=pw.IntegerField, default=[])
    roles_edit: List[UserRole] = EnumArrayField(enum_class=UserRole, field_class=pw.IntegerField, default=[])
    participants: List[User] = pw.ManyToManyField(User, backref='thing_participations')

    ip = pw.IPField(index=True, null=True)

    creator = pw.ForeignKeyField(User, backref='things')

    class Meta:
        from my_app.factory import database
        database = database

    @property
    def ago(self):
        return humanize.naturaltime(self.created)

    @classmethod
    async def new_ticket(cls, user: User, title: str, markdown: str, remote_address: str) -> 'Thing':
        if not title:
            raise Exception("title cannot be empty")
        if not validate_ipv4(remote_address):
            raise Exception("upload ipv4 address invalid")

        return cls.create(
            title=title,
            markdown=markdown,
            creator=user,
            ip=remote_address
        )

UserThingParticipant = Thing.participants.get_through_model()
```
