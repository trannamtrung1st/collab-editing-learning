# See https://aka.ms/containerfastmode to understand how Visual Studio uses this
# Dockerfile to build your images for faster debugging.

FROM mcr.microsoft.com/dotnet/aspnet:8.0.3-alpine3.19-arm64v8 AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:8.0.203-alpine3.19-arm64v8 AS build
WORKDIR /src
COPY ["WopiHost/src/WopiHost/WopiHost.csproj", "WopiHost/src/WopiHost/"]
RUN dotnet restore "WopiHost/src/WopiHost/WopiHost.csproj"
COPY . .
WORKDIR "/src/WopiHost/src/WopiHost"
RUN dotnet build "WopiHost.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "WopiHost.csproj" -c Release -o /app/publish

FROM base AS final

WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "WopiHost.dll"]