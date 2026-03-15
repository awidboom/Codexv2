import { useEffect, useState } from 'react';
import SccPage from './SccPage';
import Ap42Page from './Ap42Page';

const getRoute = () => {
  const hash = window.location.hash.replace('#', '').trim();
  return hash || '/';
};

export default function App() {
  const [route, setRoute] = useState(getRoute());

  useEffect(() => {
    const handleChange = () => setRoute(getRoute());
    window.addEventListener('hashchange', handleChange);
    return () => window.removeEventListener('hashchange', handleChange);
  }, []);

  if (route.startsWith('/ap42')) {
    return <Ap42Page />;
  }

  return <SccPage />;
}
