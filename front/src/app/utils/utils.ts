
export function toInteger(value: any): number {
  return parseInt(`${value}`, 10);
}


export function padNumber(value: number) {
  if (isNumber(value)) {
    return `${value}`.padStart(2, '0');
  } else {
    return '';
  }
}


export function isNumber(value: any): boolean {
  return !isNaN(toInteger(value));
}


export function isInteger(value: any): boolean {
  return typeof value === 'number' && isFinite(value) && Math.floor(value) === value;
}


export function isString(value: any): boolean {
  return Object.prototype.toString.call(value) === "[object String]";
}


export function isArray(value: any): boolean {
  return Object.prototype.toString.call(value) === "[object Array]";
}


export function isFunction(value) : boolean {
  return Object.prototype.toString.call(value) === "[object Function]";
}


export function isObject(o) {
  return o === Object(o) && !isArray(o) && typeof o !== 'function';
}


export function isSetsEqual(a, b) {
  if (a.size != b.size) {
    return false;
  }
  else {
    for (let x of b) {
      if (!a.has(x)) {
        return false;
      }
    }
    return true;
  }
}


export function snakeToCamel(string) {
  return string.replace(/(_\w)/g, function(m){
    return m[1].toUpperCase();
  });
}


export function keysToCamel(o) {
  if (isObject(o)) {
    const n = {};

    Object.keys(o)
      .forEach((k) => {
        n[snakeToCamel(k)] = keysToCamel(o[k]);
      });

    return n;
  } else if (isArray(o)) {
    return o.map((i) => {
      return keysToCamel(i);
    });
  }

  return o;
};


export function camelToSnake(string) {
  return string.replace(/[\w]([A-Z0-9])/g, function(m) {
    return m[0] + "_" + m[1];
  }).toLowerCase();
}


export function keysToSnake(o) {
  if (isObject(o) && !(o instanceof Date)) {
    const n = {};

    Object.keys(o)
      .forEach((k) => {
        n[camelToSnake(k)] = keysToSnake(o[k]);
      });

    return n;
  } else if (isArray(o)) {
    return o.map((i) => {
      return keysToSnake(i);
    });
  }

  return o;
};


export function arrayToMap<KeyT, ValueT>(array: any[], keyFn: Function) : Map<KeyT, ValueT> {
  let m = new Map();

  for (let x of array) {
    m.set(keyFn(x), x);
  }

  return m;
}


export function arrayDistinct<KeyT>(arr, keyFn: (any) => KeyT) {
  let s = new Set<KeyT>();
  let result = [];
  for (let x of arr) {
    let key = keyFn(x);
    if (!s.has(key)) {
      result.push(x);
      s.add(key);
    }
  }
  return result;
}


export class SuperMap<Key, Value> extends Map<Key, Value> {
  get(key: Key, defaultValue?: Value) : Value {
    if (this.has(key)) {
      return super.get(key);
    }
    else {
      return defaultValue;
    }
  }
}


export class DefaultMap<Key, Value> extends SuperMap<Key, Value> {
  defaultFactory: (Key) => Value;

  constructor(defaultFactory: (Key) => Value, iterable?) {
    super(iterable);
    this.defaultFactory = defaultFactory;
  }

  get(key: Key, defaultValue?: Value) : Value {
    if (this.has(key)) {
      return super.get(key);
    }
    else if (defaultValue === undefined) {
      return this.defaultFactory(key);
    }
    else {
      return defaultValue;
    }
  }
}


/*
 * Remove all accents and set to lower case.
 */
export function normalizeString(value: string) : string {
  return value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}


export function compareValues(key, order = 'asc') {
  return function innerSort(a, b) {
    if (!isFunction(key)) {
      if (!a.hasOwnProperty(key) || !b.hasOwnProperty(key)) {
        // property doesn't exist on either object
        return 0;
      }
    }

    const varA = isFunction(key) ? key(a) : a[key];
    const varB = isFunction(key) ? key(b) : b[key];

    let comparison = 0;

    if (isString(varA) && isString(varB)) {
      comparison = varA.localeCompare(varB);
    }
    else {
      if (varA > varB) {
        comparison = 1;
      } else if (varA < varB) {
        comparison = -1;
      }
    }

    return ((order === 'desc') ? -1 : 1 ) * comparison;
  };
}
