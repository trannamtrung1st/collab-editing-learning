# See https://aka.ms/containerfastmode to understand how Visual Studio uses this
# Dockerfile to build your images for faster debugging.

FROM mcr.microsoft.com/dotnet/aspnet:8.0.3-alpine3.19-arm64v8 AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:8.0.203-alpine3.19-arm64v8 AS build
WORKDIR /src
COPY ["WopiHost/src/WopiHost.Web/WopiHost.Web.csproj", "WopiHost/src/WopiHost.Web/"]
RUN dotnet restore "WopiHost/src/WopiHost.Web/WopiHost.Web.csproj"
COPY . .
WORKDIR "/src/WopiHost.Web/src/WopiHost.Web"
RUN dotnet build "WopiHost.Web.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "WopiHost.Web.csproj" -c Release -o /app/publish

FROM base AS final

WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "WopiHost.Web.dll"]