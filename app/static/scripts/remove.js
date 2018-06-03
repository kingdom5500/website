function remove(id) {
    var form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", "/admin");

    var hiddenField = document.createElement("input");
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("name", "delete");
    hiddenField.setAttribute("value", id);

    form.appendChild(hiddenField);

    document.body.appendChild(form);
    form.submit();
}