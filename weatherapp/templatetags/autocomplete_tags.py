from django import template

register = template.Library()


@register.simple_tag
def autocomplete_js():
    return """
    <script>
        $(document).ready(function () {
            $('#city').autocomplete({
                source: '{% url "autocomplete_city" %}',
                minLength: 2
            });
        });
    </script>
    """
