from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.admin.options import StackedInline
from .models import *
from modeltranslation.admin import TranslationAdmin

# Here we describe the class for ckeditor widget:
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    """ Class of ModelForm where we have the field with CKEditorWidget,
    but we will use CKEditorUploadingWidget to have and opportunity to upload images """

    # This is our field with CKEditorWidget or CKEditorUploadingWidget.
    # The name of current field is the same as in Movie model
    description_ru = forms.CharField(label='Description', widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label='Description', widget=CKEditorUploadingWidget())

    class Meta:
        # We use Movie model just because we want to work with it:
        model = Movie
        fields = '__all__'


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Category admin class with options """

    list_display = ('id', 'name', 'url')
    # By default, Django use the id field as link to go to page with edit form, but we can add other fields too with
    # link_display_links param
    list_display_links = ('name',)


class ReviewInline(admin.TabularInline):
    """ This is an StackedInline class to see all reviews for movie. We can see them when we look at the movie.
    Also, we can use TabularInline. It will change the layout for Review forms as a tabel with fields to edit """

    model = Reviews
    # EXTRA attribute is used for specify the count of creations forms to seed.
    # By default - 3 (we will see 3 forms to create reviews under the movie edit form):
    extra = 1
    readonly_fields = ('name', 'email')


class MovieShotsInLine(admin.TabularInline):
    model = MovieShots
    extra = 1
    # Image field and get_image field are not the same!
    # Image - from our model, get_image - new field for display the preview of our image.
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        """
        Current method get the obj - current actor object
        :param obj: Current MovieShot object from models.py
        :return: MarkSafe string with img-html-tag to display current MovieShot image
        """

        # Method mark_safe is used to display html tags not as simple string but like a working html-tag.
        # This method mark string with html for django like a safe string, which can be used like a tag:
        return mark_safe(f'<img src={obj.image.url} width="60" height="80" style="object-fit: cover;"')

    get_image.short_description = 'Image Preview'


@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    """ Movie admin class with options """

    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    # if in search field we will use only category without __name, we will search by category_id (by its number):
    search_fields = ('title', 'category__name')
    # This attribute can work with M2M fields and ForeignKey fields:
    inlines = [MovieShotsInLine, ReviewInline]
    # To enable to save movie form on top of the page:
    save_on_top = True
    # Enable to change only some fields with keeping all other data and save the object as new object into the db:
    save_as = True
    # Attribute to specify fields to add them without opening the edit form:
    list_editable = ('draft',)
    # ACTIONS attribute is used to add our own actions into admin model:
    # We can see these actions in the drop-down list of actions when viewing our table
    actions = ['mark_as_draft', 'unmark_as_draft']
    # With FORM attribute we can specify the form class which we want to use for current model in django-admin panel:
    form = MovieAdminForm
    # Poster field and get_image field are not the same!
    # Image - from our model, get_image - new field for display the preview of our image.
    readonly_fields = ('get_image',)
    # With FIELDS attribute we can specify fields which we want to see in one row and only fields in FIELDS attribute we
    # will see in our forms, all others will be deleted:
    # fields = (('actors', 'directors', 'genres'),)

    # More useful attribute to group our fields:
    fieldsets = (
        # The first value before dictionary it is the group name:
        (None, {
            # Tuple in tuple we use when we need to display fields as one row:
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': ('description', ('poster', 'get_image'))
        }),
        (None, {
            'fields': (('year', 'world_premier', 'country'),)
        }),
        ('Actors', {
            # In current classes key we can add classes for group. In such case, we say that we want te see our group in
            # collapse (свернутом) mode.
            'classes': ('collapse',),
            'fields': (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        ("Options", {
            'fields': (('url', 'draft'),)
        }),
    )

    def get_image(self, obj):
        """
        Current method get the obj - current actor object
        :param obj: Current Movie object from models.py
        :return: MarkSafe string with img-html-tag to display current movie poster
        """

        # Method mark_safe is used to display html tags not as simple string but like a working html-tag.
        # This method mark string with html for django like a safe string, which can be used like a tag:
        return mark_safe(f'<img src={obj.poster.url} width="60" height="80" style="object-fit: cover;"')

    def mark_as_draft(self, request, queryset, draft_value=True):
        """ Action for admin model to unpublished movies """

        updated_count = queryset.update(draft=draft_value)
        message_bit = 'One row was updated' if updated_count == 1 else f'{updated_count} were updated'
        self.message_user(request, message=message_bit)

    def unmark_as_draft(self, request, queryset):
        """ Action for admin movie model to publish movies """

        self.mark_as_draft(request, queryset, draft_value=False)

    mark_as_draft.short_description = 'Mark selected as draft'
    # Specify user permissions to use current action:
    mark_as_draft.allowed_permissions = ('change',)

    unmark_as_draft.short_description = 'Unmark selected as draft'
    # Specify user permissions to use current action:
    unmark_as_draft.allowed_permissions = ('change',)

    get_image.short_description = 'Poster Preview'


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """ Reviews admin class with options """

    list_display = ('id', 'name', 'email', 'parent', 'movie')
    # Specify fields which we could not be able to edit:
    read_only_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    """ Genre admin class with options """
    list_display = ('id', 'name', 'url')


@admin.register(Actor)
class ActorAdmin(TranslationAdmin):
    """ Actor admin class with options """

    list_display = ('id', 'name', 'age', 'image', 'get_image')

    # Image field and get_image field are not the same!
    # Image - from our model, get_image - new field for display the preview of our image.
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        """
        Current method get the obj - current actor object
        :param obj: Current Actor object from models.py
        :return: MarkSafe string with img-html-tag to display current actor image
        """

        # Method mark_safe is used to display html tags not as simple string but like a working html-tag.
        # This method mark string with html for django like a safe string, which can be used like a tag:
        return mark_safe(f'<img src={obj.image.url} width="50" height="60" style="object-fit: cover;"')

    # Here we make new column name for work of our method
    get_image.short_description = 'Image Preview'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """ Rating admin class with options """
    list_display = ('id', 'ip', 'star', 'movie')


@admin.register(MovieShots)
class MovieShotsAdmin(TranslationAdmin):
    """ MovieShots admin class with options """
    list_display = ('id', 'movie', 'image', 'get_image')

    # Image field and get_image field are not the same!
    # Image - from our model, get_image - new field for display the preview of our image.
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        """
        Current method get the obj - current actor object
        :param obj: Current MovieShot object from models.py
        :return:
        """

        # Method mark_safe is used to display html tags not as simple string but like a working html-tag.
        # This method mark string with html for django like a safe string, which can be used like a tag:
        return mark_safe(f'<img src={obj.image.url} width="60" height="80" style="object-fit:cover;"')

    # Here we make new column name for work of our method
    get_image.short_description = 'Image Preview'


admin.site.register(RatingStar)

# With this param we can replace the default django-admin page title:
admin.site.site_title = 'Django Movies Project'
# With this param we can replace the default django-admin panel on the top of the page:
admin.site.site_header = 'Django Movies Project'
