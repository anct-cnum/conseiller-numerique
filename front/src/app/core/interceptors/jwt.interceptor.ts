import {Injectable} from '@angular/core';
import {HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {Observable} from 'rxjs';
import {AuthService} from 'app/core/services/auth.service';
import {environment} from '@env';


@Injectable()
export class JwtInterceptor implements HttpInterceptor {

  constructor(private auth: AuthService) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Only intercept api requests
    if (!request.url.startsWith(environment.apiUrl)) {
      return next.handle(request);
    }

    // Get token
    const token = this.auth.token;

    // If no token, skip
    if (!this.auth.token) {
      return next.handle(request);
    }

    // Inject token
    request = request.clone({
      headers: request.headers.set('Authorization',
        'Bearer ' + token)
    });

    return next.handle(request);
  }
}
