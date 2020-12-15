import { Injectable } from '@angular/core';
import {BehaviorSubject, Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {environment} from '@env';
import {Login} from 'app/core/dao/login';
import {finalize, tap} from 'rxjs/operators';
import {User} from 'app/core/dao/user';
import {JwtHelperService} from '@auth0/angular-jwt';


export const KEY_TOKEN = 'cnumToken';
export const KEY_USER = 'user';


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private _token$ = new BehaviorSubject<string>(null);
  private _user$ = new BehaviorSubject<User>(null);
  private _authenticating$ = new BehaviorSubject<boolean>(false);

  private _url = '';

  constructor(private _http: HttpClient,
              private _router: Router) {
    this._url = `${environment.apiUrl}/api/auth`;
    this.readToken();
  }

  isAuthenticated(): boolean {
    return !!this.token;
  }

  public authenticate(login: Login): Observable<any> {
    this._authenticating$.next(true);
    return this._http.post<any>(`${this._url}/token`, login).pipe(
      tap(res => {
        const helper = new JwtHelperService();
        const accessToken = res.access;
        const user = helper.decodeToken<User>(accessToken);
        this._token$.next(accessToken);
        this._user$.next(user);
        sessionStorage.setItem(KEY_TOKEN, accessToken);
        sessionStorage.setItem(KEY_USER, JSON.stringify(user));
      }),
      finalize(() => this._authenticating$.next(false))
    );
  }

  /*
  public resetPassword(resetPassword: ResetPassword): Observable<any> {
    return this._http.post<any>(`${this._url}/reset-password`, resetPassword);
  }

  public forgotPassword(email: string): Observable<any> {
    return this._http.post<any>(`${this._url}/reset-password/${email}`, {});
  }
  */

  public logout(redirectUrl = ''): void {
    sessionStorage.clear();
    this._token$.next(null);
    this._user$.next(null);
    this._router.navigateByUrl(redirectUrl).then(() => window.location.reload());
  }

  /**
   * PRIVATE FUNCTIONS
   */

  private readToken(): void {
    const token = sessionStorage.getItem(KEY_TOKEN);
    if (!token) {
      return;
    }
    this.token$.next(token);
    const sUser = sessionStorage.getItem(KEY_USER);
    if (sUser) {
      let user;
      try {
        user = JSON.parse(sUser);
      } catch (Error) {
        console.error('Cannot parse user', sUser);
        this.logout();
        return;
      }
      this.user$.next(user);
    }
  }

  /**
   * GETTERS
   */

  public get authenticating$(): Observable<boolean> {
    return this._authenticating$;
  }

  public get token$(): BehaviorSubject<string> {
    return this._token$;
  }

  public get token(): string {
    return this._token$.value;
  }

  public get user$(): BehaviorSubject<User> {
    return this._user$;
  }

  public get user(): User {
    return this._user$.value;
  }
}
