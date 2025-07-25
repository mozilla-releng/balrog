function getDefaultFontSize() {
  const parent = document.body;
  const element = document.createElement('div');

  element.style.cssText =
    'display:inline-block; padding:0; line-height:1; position:absolute; visibility:hidden; font-size:1rem';

  element.appendChild(document.createTextNode('M'));
  parent.appendChild(element);

  const size = element.offsetHeight;

  parent.removeChild(element);

  return size;
}

export default (value) => parseFloat(value) * getDefaultFontSize();
