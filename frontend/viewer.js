import { LitElement, html, css } from  'https://unpkg.com/lit-element@latest/lit-element.js?module';

class Viewer extends LitElement {
  static get properties() {
    return {
      id: {
        type: String,
        reflected: true
      },
      tags: {
        type: Array
      }
    }
  }

  constructor() {
    super();
  }

  static get styles() {
    return css`
      img {
        width: 100%;
      }
    `;
  }

  render() {
    return html`
      <link rel="stylesheet" href="css/skeleton.css">
      <link rel="stylesheet" href="css/normalize.css">
      <div class="container">
        <div class="row">
          <div class="twelve columns">
            <time>${this.datePublished}</time>
            <a href=${this.link}>●</a>
          </div>
        </div>
        <div class="row">
          <div class="twelve columns">
            <img alt="comic" src="comics/webcomicname.com/media/tumblr_ptptjhhVb41qg1n95_1280.png">
          </div>
        </div>
        <div class="row">
          <div class="column">
            ${this.tags.map(tag => html`<a href=${tag.href}>${tag.name}</a>&nbsp`)}
          </div>
        </div>
        <div class="row">
          <div class="three columns">
            <a class="button" href="#">< Previous</a>
          </div>
          <div class="six columns">&nbsp</div>
          <div class="three columns">
            <a class="button" href="#">Next ></a>
          </div>
        </div>
      </div>
    `;
  }
}

window.customElements.define('webcomics-viewer', Viewer);
