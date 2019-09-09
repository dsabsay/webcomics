javascript:(function(){
  const form = document.createElement('form');
  form.setAttribute('action', 'http://localhost:5000/bookmark');
  form.setAttribute('method', 'POST');

  const input = document.createElement('input');
  input.setAttribute('type', 'text');
  input.setAttribute('name', 'bookmark_url');
  input.value = location.href;

  form.append(input);
  document.body.append(form);

  form.submit();
})();
