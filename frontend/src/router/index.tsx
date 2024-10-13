import React, { ReactNode, memo } from "react";

import { Navigate, Route, Routes, useLocation } from "react-router-dom";

import { StartPage } from "../components/StartPage";

type TRouteType = {
  path: string;
  element: ReactNode;
};

const AppRouter: React.FC = () => {
  const location = useLocation();
  const isAuth = !!sessionStorage.getItem("userToken");

  /** Список доступных публичных страниц */
  const publicRoutes: TRouteType[] = [{ path: "/", element: <StartPage /> }];

  /** Список доступных приватных страниц */
  const privateRoutes: TRouteType[] = [
    ...publicRoutes,
    ...[
      // { path: "/cabinet", element: <AllSites /> },
    ],
  ];

  /** Страница входит в список приватных ? */
  const isPrivatePage = findPageInList(privateRoutes);
  /** Страница входит в список публичных ? */
  const isPublicPage = findPageInList(publicRoutes);

  /** Функция для нахождения текущей странице в списке доступных */
  function findPageInList(list: TRouteType[]) {
    return list.findIndex(comp => comp.path === location.pathname) !== -1;
  }

  if (!isPrivatePage || !isPublicPage) {
    return <Navigate to="/" />;
  }

  if (isAuth) {
    return (
      <Routes>
        {privateRoutes.map(({ path, element }, index) => (
          <Route
            path={path}
            element={element}
            key={`${path}_${index}`}
          />
        ))}
      </Routes>
    );
  }

  return (
    <Routes>
      {publicRoutes.map(({ path, element }, index) => (
        <Route
          path={path}
          element={element}
          key={`${path}_${index}`}
        />
      ))}
    </Routes>
  );
};

AppRouter.displayName = "AppRouter";

export default memo(AppRouter);
