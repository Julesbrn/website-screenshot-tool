import { Component } from '@angular/core';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'siteScreenShot';
  url = ""

  urlForUser: string = "";

  constructor() { }


  doBtn(box: any)
  {
    this.isLoaded = "loading";
    this.url = "/getImg/" + encodeURIComponent(encodeURIComponent(box.value)); //We need to double encode to bypass flask bug. See flask comment.
    this.urlForUser = window.location.href + "getImg/" + encodeURIComponent(encodeURIComponent(box.value)); //We need to double encode to bypass flask bug. See flask comment.
  }

  doBtnHelper(box: any)
  {
    this.urlForUser = window.location.href + "getImg/" + encodeURIComponent(encodeURIComponent(box.value)); //We need to double encode to bypass flask bug. See flask comment.
  }

  urls: Array<string> = [];
  urlBase: string = "";
  doBtnMulti(box: any)
  {
    this.urls = new Array<string>();
    var tmp_urls = box.value.split("\n"); //We need to double encode to bypass flask bug. See flask comment..split("\n");
    console.log(tmp_urls)
    this.urlBase = window.location.href.slice(0, -1);
    for(let url of tmp_urls)
    {
      console.log(url);
      this.urls.push("/getImg/" + encodeURIComponent(encodeURIComponent(url)))
    }
    console.log(this.urls);
    this.isLoaded = "loading";
    //this.url = "/getImg/" + encodeURIComponent(encodeURIComponent(box.value)); //We need to double encode to bypass flask bug. See flask comment.
    this.urlForUser = window.location.href + "getImg/" + encodeURIComponent(encodeURIComponent(box.value)); //We need to double encode to bypass flask bug. See flask comment.
  }

  type:string = "single"
  setType(str: string)
  {
    this.urls = new Array<string>();
    this.urlForUser = "";
    this.isLoaded = "init";
    this.url = "";

    this.type = str;
  }

  isLoaded: string = "init";

  onImageLoad(evt: any) 
  {
    if (evt && evt.target) 
    {
      this.isLoaded = "success";
      const width = evt.target.naturalWidth;
      const height = evt.target.naturalHeight;
      const portrait = height > width ? true : false;
      console.log(width, height, 'portrait: ', portrait);
    }
    else
    {
      this.isLoaded = "error";
    }
  }
}
