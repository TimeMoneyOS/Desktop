document.addEventListener('DOMContentLoaded', () => {
  const dialog = document.createElement('dialog');
  dialog.className = 'wave-viewer';
  dialog.setAttribute('aria-label', '图示放大');
  const close = document.createElement('button');
  close.textContent = '\u00d7';
  close.setAttribute('aria-label', '关闭图示');
  close.title = '关闭图示';
  const image = document.createElement('img');
  dialog.append(close, image);
  document.body.append(dialog);
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', e => { if (e.target === dialog) dialog.close(); });
  document.querySelectorAll('.md-content img').forEach(source => {
    source.tabIndex = 0;
    const open = () => {
      image.src = source.src;
      image.alt = source.alt;
      dialog.showModal();
    };
    source.addEventListener('click', open);
    source.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
    });
  });
});
