import { LitElement, html, css } from  'https://unpkg.com/lit-element@latest/lit-element.js?module';
import './comic.js';
import './viewer.js';

class App extends LitElement {
  static get properties() {
    return {
      comics: { type: Array }
    }
  }

  constructor() {
    super();

    this.comics = [
      {
        name: 'xkcd',
        link: 'https://xkcd.com/',
        iconUrl: 'https://xkcd.com/s/919f27.ico',
        numUnread: 3,
        isOpen: false,
        strips: []
      },
      {
        name: 'Nedroid',
        link: 'http://nedroid.com/',
        iconUrl: 'http://nedroid.com/favicon.ico',
        numUnread: 2,
        isOpen: true,
        strips: [
          {
            title: 'Fruit Pursuit',
            link: 'http://nedroid.com/2019/08/fruit-pursuit/',
            publishedDate: new Date('Fri, 23 Aug 2019 15:25:33 +0000'),
            wasRead: false
          },
          {
            title: 'No Purchase Necessary',
            link: 'http://nedroid.com/2019/08/no-purchase-necessary/',
            publishedDate: new Date('Mon, 19 Aug 2019 14:58:36 +0000'),
            wasRead: true
          },
          {
            title: 'Farmer Fruitley’s Orchard',
            link: 'http://nedroid.com/2019/08/farmer-fruitleys-orchard/',
            publishedDate: new Date('Thu, 15 Aug 2019 14:05:53 +0000'),
            wasRead: true
          }
        ]
      }
    ];
  }

  render() {
    return html`
      <link rel="stylesheet" href="css/skeleton.css">
      <link rel="stylesheet" href="css/normalize.css">
      <div class="container">
        <div class="row">
          <h1 class="twelve columns">Web Comics</h1>
        </div>

        ${this.comics.map(comic => html`
          <div class="row">
            <webcomics-comic
              name=${comic.name}
              link=${comic.link}
              iconUrl=${comic.iconUrl}
              numUnread=${comic.numUnread}
              isOpen=${comic.isOpen}
              .strips=${comic.strips}
            ></webcomics-comic>
          </div>`
        )}
      </div>
      <webcomics-viewer
        id=169627548649
        .tags=${[
          {href: 'http://webcomicname.com/tagged/comics', name: '#comics'},
          {href: 'http://webcomicname.com/tagged/oh%20no', name: '#oh no'}
        ]}>
      </webcomics-viewer>
    `;
  }
}

window.customElements.define('webcomics-app', App);
