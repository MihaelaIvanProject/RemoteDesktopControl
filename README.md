# RemoteDesktopControl
Controlul unei aplicatii desktop prin web folosind WebSocket.

Cloneaza repository-ul si instaleaza dependintele Python:

```bash
git clone https://github.com/MihaelaIvanProject/RemoteDesktopControl.git
cd RemoteDesktopControl
pip install -r requirements.txt
```

Porneste serverul:

```bash
python server.py
```

Porniti aplicatia desktop (unde „client” este identificatorul acestui client):

```bash
python desktop.py client
```

Deschideti `web.html` in browser, introduceti `client` (la fel ca cel pe care l-ati furnizat pentru desktop) in campul de introducere si faceti clic pe *Conectati*.

Acum ar trebui sa vedeti utilizarea CPU raportata pe pagina web. Daca faceti click pe *Beep*, computerul ar trebui sa emita un sunet.

