import { Injectable } from '@angular/core';
import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiAdapter } from 'app/core/services/api/adapter';
import { map } from 'rxjs/operators';
import { environment } from '@env';


@Injectable()
export class ApiAdapterInterceptor implements HttpInterceptor {

  constructor() {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    if (!request.url.startsWith(environment.apiUrl)) {
      return next.handle(request);
    }

    request = request.clone({
      body: ApiAdapter.app2api(request.body),
    });
    return next.handle(request).pipe(
      map((event: HttpEvent<any>) => {
        console.log('event api adapter', event);
        if (event instanceof HttpResponse) {
          return event.clone({
            body: ApiAdapter.api2app(event.body),
          });
        }
        return event;
      }),
    );
  }
}
