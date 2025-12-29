const tg = window.Telegram.WebApp;
tg.expand();

function collect() {
  tg.sendData("collect");
}
